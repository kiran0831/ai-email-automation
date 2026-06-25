import schedule
import time
import os, json, base64, re, requests
from dotenv import load_dotenv
from groq import Groq
from googleapiclient.discovery import build
from gmail_auth import authenticate
from datetime import datetime


# -----------------------
# ENV
# -----------------------
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------
# GMAIL SETUP
# -----------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
creds = authenticate(SCOPES)
service = build('gmail', 'v1', credentials=creds)

# -----------------------
# TIME FORMAT
# -----------------------
def format_gmail_time(ms):
    return datetime.fromtimestamp(int(ms) / 1000).strftime("%Y-%m-%d %H:%M:%S")

# -----------------------
# BODY EXTRACTION
# -----------------------
def extract_body(msg):
    payload = msg.get("payload", {})

    body = payload.get("body", {}).get("data")
    if body:
        return base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""

# -----------------------
# LABELS
# -----------------------
def get_label_ids():
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    return {x["name"]: x["id"] for x in labels}

# -----------------------
# CLASSIFIER (CLEAN)
# -----------------------
def classify_email(subject, body):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an email classifier.
Classify this email into exactly one of these categories:

Internships - emails about internships, job offers, hiring, offer letters, or recruitment
AI & Tech - emails about coding, hackathons, coding competitions, AI, data science, machine learning, or any tech-related topics
Others - anything that does not fit the above two categories

Reply with only the category name exactly as written above. Nothing else. No punctuation, no explanation.

DO NOT classify these as Internships or AI & Tech, classify as Others:
- Google security alerts
- Account access notifications
- Login/password alerts
- Any email from no-reply@accounts.google.com
- Any email about account activity or security
- Bulk digest emails listing multiple opportunities (LinkedIn alerts, Unstop newsletters)"""
            },
            {
                "role": "user",
                "content": f"Subject: {subject}\nBody: {body[:1000]}"
            }
        ]
    )

    category = response.choices[0].message.content.strip()

    # FIX LABEL MISMATCH
    label_map = {
        "AI": "AI & Tech",
        "AI & Tech": "AI & Tech",
        "Internships": "Internships",
        "Others": "Others"
    }

    return label_map.get(category, "Others")

# -----------------------
# APPLY LABEL
# -----------------------
def add_label(msg_id, label_id, category):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={"addLabelIds": [label_id]}
    ).execute()

    print("Labeled:", category)

# -----------------------
# ALERT SYSTEM (FIXED JSON)
# -----------------------
def alerts_email(subject, sender, snippet, body, message_id, email_time,category):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an email filter assistant for a student tracking internships and tech opportunities.

Only reply SKIP if the email is clearly:
- Promotional or marketing
- A newsletter with no action required
- A security/account alert
- Completely irrelevant to internships or tech opportunities

If the email contains ANY of these → process it:
- Internship or job opportunity
- Interview call or invitation
- Offer letter
- Registration for a hackathon or event
- Deadline reminder
- Any email requiring action

Reply with only this JSON:
{
  "company": "",
  "label": "",
  "type": "",
  "role": "",
  "deadline": "",
  "link": ""
}
Return only JSON. No extra text. No markdown. No backticks.
If SKIP, reply only: SKIP"""
            },
            {
                "role": "user",
                "content": f"From: {sender}\nSubject: {subject}\nBody: {body[:1000]}"
            }
        ]
    )

    output = response.choices[0].message.content.strip()

    # CLEAN MODEL OUTPUT
    output = re.sub(r"^JSON:\s*", "", output)
    output = output.replace("```", "").strip()

    if output == "SKIP":
        print("Skipped email")
        return

    try:
        data = json.loads(output)
    except Exception:
        print("JSON error:", output)
        return

    embed = {
    "embeds": [{
        "title": f"🔔 New {category} Email",
        "color": 5814783,
        "fields": [
            {"name": "🏢 Company", "value": data.get('company', 'N/A'), "inline": True},
            {"name": "📌 Type", "value": data.get('type', 'N/A'), "inline": True},
            {"name": "💼 Role", "value": data.get('role', 'N/A'), "inline": True},
            {"name": "⏰ Deadline", "value": data.get('deadline', 'N/A'), "inline": True},
            {"name": "🔗 Link", "value": data.get('link', 'N/A'), "inline": False},
            {"name": "📬 Open Mail", "value": f"https://mail.google.com/mail/u/0/#inbox/{message_id}", "inline": False}
        ],
        "footer": {"text": f"📅 {email_time}"}
    }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=embed)

    print("Alert sent ✔")

# -----------------------
# MAIN PIPELINE
# -----------------------
def get_emails():

    results = service.users().messages().list(
    userId='me',
    q='newer_than:6h'
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No messages found")
        return

    labels = get_label_ids()

    for message in messages:

        msg = service.users().messages().get(
            userId='me',
            id=message['id'],
            format="full"
        ).execute()

        headers = msg.get('payload', {}).get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')

        body = extract_body(msg)
        snippet = msg.get("snippet", "")

        if not body:
            body = snippet

        body = body[:1000]

        email_time = format_gmail_time(msg.get("internalDate"))

        category = classify_email(subject, body)

        if category == "Others":
            print("Skipped as Others")
            continue

        label_id = labels.get(category)

        if not label_id:
            print("Label not found:", category)
            continue

        if label_id in msg.get("labelIds", []):
            print("Already labeled:", category)
            continue

        add_label(message['id'], label_id, category)

        alerts_email(
            subject,
            sender,
            snippet,
            body,
            message['id'],
            email_time
            ,category
        )

# -----------------------
# RUN
# -----------------------
get_emails()

# Then run every 6 hours
schedule.every(6).hours.do(get_emails)

print("Scheduler running — checks every 6 hours")
while True:
    schedule.run_pending()
    time.sleep(60)
    

📧 AI Internship Email Notifier
An intelligent email automation workflow built with N8N that monitors Gmail every 6 hours, uses AI to classify and filter emails, and sends only relevant opportunities to Telegram — with automatic logging to Google Sheets.

⚙️ How It Works

⏰ Schedule Trigger — runs every 6 hours automatically
📧 Fetch Emails — gets all new emails via Gmail API
🤖 LLM Pass 1 — classifies emails into Internships, AI & Tech, or Others using LLaMA 3.3 70B
🏷️ Auto Label — applies the label directly in Gmail
🤖 LLM Pass 2 — decides if the email is worth notifying (skips promotions, newsletters, alerts)
📊 Log to Sheets — saves company, role, deadline, and links to Google Sheets
📲 Telegram Alert — sends a formatted notification with all key details


🛠️ Tech Stack

N8N — workflow automation
Gmail API — fetch and label emails
Groq API (LLaMA 3.3 70B) — AI classification and filtering
Google Sheets API — logging opportunities
Telegram Bot API — real-time notifications


🚀 Setup

Import internship_email_notifier.json into N8N
Connect credentials: Gmail, Groq, Google Sheets, Telegram
Replace YOUR_TELEGRAM_CHAT_ID and YOUR_GOOGLE_SHEET_ID with your values
Create Gmail labels: Internships and AI & Tech
Activate the workflow ✅


👤 Author
Kiran Reddy Kandi · GitHub · LinkedIn

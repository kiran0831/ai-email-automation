# 🤖 AI Email Classifier & Alert System

> Automatically classifies Gmail every 6 hours using LLaMA 3.3 70B and sends Discord alerts for internships and tech opportunities.

## How It Works

1. Fetches new emails from Gmail every 6 hours
2. Classifies each email → **Internships**, **AI & Tech**, or **Others**
3. Applies Gmail label automatically
4. Extracts key details (company, role, deadline, link)
5. Sends a rich Discord alert — skips "Others" silently

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Gmail API (OAuth 2.0) | Fetch emails + apply labels |
| Groq + LLaMA 3.3 70B | Classification + extraction |
| Discord Webhooks | Real-time alerts |
| Schedule | Automated 6-hour runs |

## Setup

```bash
git clone https://github.com/kiran0831/ai-email-classifier
cd ai-email-classifier
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your_key

DISCORD_WEBHOOK_URL=your_webhook

Then set up Gmail OAuth ([Google Cloud Console](https://console.cloud.google.com)) — enable Gmail API, create OAuth 2.0 credentials (Desktop), download as `credentials.json`.

Create three Gmail labels: `Internships`, `AI & Tech`, `Others`.

```bash
python3 gmail_classifier.py
```

First run opens a browser for Gmail login. Scheduler starts automatically after.

## Discord Alert Example
🔔 New Internships Email

🏢 Company     Optum India

💼 Role        Associate AI/ML Engineer

⏰ Deadline    30 Jun 2026

🔗 Link        careers.optum.com/...

## ⚠️ Security

Never commit `credentials.json` or `token.json` — both are in `.gitignore`.

## 👨‍💻 Built By

**Kiran Reddy** — Final year CS student  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/kiran-reddy-0b2749303)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/kiran0831)

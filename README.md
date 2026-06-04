# 🤖 AI Email Automation

An intelligent, fully automated email monitoring system powered by N8N and LLaMA 3.3 70B. Watches your Gmail around the clock, uses a two-stage AI pipeline to classify and filter incoming emails, auto-labels your inbox, logs every opportunity to Google Sheets, and instantly notifies you on Telegram — so you never miss an internship, hackathon, or tech opportunity again.

---

## How It Works

1. ⏰ **Schedule Trigger** — runs every 6 hours automatically
2. 📧 **Fetch Emails** — gets all new emails from the last 6 hours via Gmail API
3. 🤖 **LLM Classification** — LLaMA 3.3 70B classifies each email as `Internships`, `AI & Tech`, or `Others`
4. 🏷️ **Auto Label** — applies the classified label directly in Gmail
5. 🤖 **LLM Filter** — second AI pass decides if the email is worth notifying (skips promotions, newsletters, alerts)
6. 📊 **Log to Sheets** — saves company, role, deadline, and links to Google Sheets
7. 📲 **Telegram Alert** — sends a formatted notification with all key details

---

## Features

- Runs fully automatically every 6 hours — no manual input needed
- Two-stage AI filtering for high accuracy
- Auto-labels Gmail inbox for better organization
- Skips already-processed emails to avoid duplicates
- Logs every opportunity with company, role, deadline, and application link
- Instant Telegram alerts with a direct Gmail link

---

## Tech Stack

- **N8N** — workflow automation
- **Gmail API** — fetch and label emails
- **Groq API (LLaMA 3.3 70B)** — AI classification and filtering
- **Google Sheets API** — opportunity logging
- **Telegram Bot API** — real-time notifications

---

## Setup

1. Import `internship_email_notifier.json` into N8N
2. Connect credentials: Gmail, Groq, Google Sheets, Telegram
3. Replace `YOUR_TELEGRAM_CHAT_ID` and `YOUR_GOOGLE_SHEET_ID` with your values
4. Create Gmail labels: `Internships` and `AI & Tech`
5. Activate the workflow ✅

---

## Author

**Kiran Reddy Kandi**

---

## 📸 Workflow

![Workflow](https://github.com/user-attachments/assets/c12f4752-527e-4893-a46a-f0c64b0b7991)

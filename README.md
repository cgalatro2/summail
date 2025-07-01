# Summail

Summail is a simple Python script that fetches your newsletter emails from Gmail, summarizes them using GPT, and sends you a daily digest.

## ✨ Features

- Authenticates with Gmail via desktop OAuth
- Fetches emails from your `Newsletters` label from the previous day
- Summarizes each email using OpenAI's GPT model
- Sends a clean summary email to your own inbox

## 🚀 Getting Started

### 1. Clone the repo and create a virtual environment

```bash
git clone https://github.com/yourusername/summail.git
cd summail
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up credentials

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a project and enable the Gmail API
- Create **OAuth 2.0 Client IDs** for a **Desktop App**
- Download the `credentials.json` and place it in the root of this project

You will also need an OpenAI API key:

```bash
export OPENAI_API_KEY=your-key-here
```

### 4. Run the script

```bash
python summail_main.py
```

## 💠 Project Structure

```
summail/
├── summail_main.py          # Entry point
├── gmail_fetcher.py         # Logic to fetch emails
├── summarizer.py            # Summarizes text via OpenAI
├── email_sender.py          # Sends the summary email
├── requirements.txt
└── credentials.json         # (gitignored) Google API OAuth credentials
```

## 📬 Output Example

```
📬 Summail Digest – June 17, 2025

=== Newsletter 1 ===
- Summary point 1
- Summary point 2
- Summary point 3

=== Newsletter 2 ===
...
```

## 🧐 Roadmap

- [ ] Add memory to avoid duplicate summaries
- [ ] Classify emails (important / unimportant / newsletters)
- [ ] Web dashboard to view summaries
- [ ] Auto-scheduling via cron

---

MIT License

# Summail - Daily Newsletter Digest

Automatically fetch and summarize your daily newsletters using Gmail API and OpenAI.

## Features

- Fetches newsletters from today (midnight to current time)
- Handles different email formats (HTML, plain text, multipart)
- Special handling for Morning Brew emails (uses Gmail snippet)
- Summarizes content using OpenAI GPT-4
- Runs daily at 5pm PST via GitHub Actions

## Local Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Gmail API credentials:**

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` and place in project root

3. **Set up OpenAI API key:**

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run locally:**
   ```bash
   python summail_digest.py
   ```

## GitHub Actions Setup

1. **Push your code to GitHub**

2. **Set up GitHub Secrets:**

   - Go to your repo → Settings → Secrets and variables → Actions
   - Add `OPENAI_API_KEY` with your OpenAI API key

3. **Set up Gmail Service Account (for CI):**

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a Service Account
   - Download the JSON key file
   - Add the entire JSON content as a GitHub secret named `GMAIL_SERVICE_ACCOUNT_KEY`

4. **Update the workflow to use the service account key:**

   ```yaml
   - name: Create service account key file
     run: echo '${{ secrets.GMAIL_SERVICE_ACCOUNT_KEY }}' > service-account-key.json
   ```

5. **The workflow will run automatically:**
   - Daily at 5pm PST (1am UTC)
   - Can be triggered manually via GitHub Actions tab

## Gmail Labels

Make sure your newsletters are labeled with "Newsletters" in Gmail for the script to find them.

## Timezone

The script uses PDT (Pacific Daylight Time, UTC-7). Adjust the timezone in `gmail_fetcher.py` if needed.

## Files

- `gmail_fetcher.py` - Gmail API integration and email processing
- `summarizer.py` - OpenAI integration for summarization
- `summail_digest.py` - Main script that orchestrates the process
- `.github/workflows/daily-digest.yml` - GitHub Actions workflow

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

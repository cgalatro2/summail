from gmail_fetcher import get_gmail_service, fetch_yesterdays_newsletters
from summarizer import summarize_email

if __name__ == "__main__":
    service = get_gmail_service()
    emails = fetch_yesterdays_newsletters(service)

    for i, email_text in enumerate(emails):
        print(f"\n=== Summary for email {i + 1} ===")
        summary = summarize_email(email_text)
        print(summary)

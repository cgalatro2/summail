from gmail_fetcher import get_gmail_service, fetch_todays_newsletters
from summarizer import summarize_email

if __name__ == "__main__":
    service = get_gmail_service()
    emails = fetch_todays_newsletters(service)

    print(f"Found {len(emails)} emails:")
    for i, email in enumerate(emails):
        print(f"\n=== {email['subject']} ({email['from']}) ===")
        summary = summarize_email(email['body'])
        print(summary)
from gmail_fetcher import get_gmail_service, fetch_todays_newsletters, send_digest_email
from summarizer import summarize_email

if __name__ == "__main__":
    service = get_gmail_service()
    emails = fetch_todays_newsletters(service)

    print(f"Found {len(emails)} emails:")
    digest_html = ["<h2>Today's Newsletter Digest</h2>"]
    for i, email in enumerate(emails):
        subject = email['subject']
        sender = email['from']
        # summary = summarize_email(email['body'])
        digest_html.append(f"<h3>{subject} <span style='font-weight:normal;'>({sender})</span></h3>")
        # digest_html.append(f"<ul>" + ''.join(f"<li>{line.strip()}</li>" for line in summary.split('\n') if line.strip()) + "</ul>")

    digest_html = '\n'.join(digest_html)
    message = {
        'to_email': "chasegalatro@gmail.com",
        'subject': "Today's Newsletter Digest",
        'html_content': digest_html
    }
    send_digest_email(service, **message)
    print("Digest sent!")
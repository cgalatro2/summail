from gmail_utils import get_gmail_service, fetch_unread_newsletters, send_digest_email
from summarizer import summarize_email
from datetime import datetime

if __name__ == "__main__":
    # Check if it's a weekend (Saturday = 5, Sunday = 6)
    current_day = datetime.now().weekday()
    if current_day >= 5:  # Saturday or Sunday
        print("Weekend detected - skipping digest generation")
        exit()

    service = get_gmail_service()
    emails = fetch_unread_newsletters(service, mark_as_read=True)

    print(f"Found {len(emails)} emails")
    digest_html = ["<h2>Today's Newsletter Digest</h2>"]
    for i, email in enumerate(emails):
        subject = email["subject"]
        sender = email["from"]
        message_id = email["message_id"]
        thread_id = email["thread_id"]

        # Create Gmail link
        gmail_link = f"https://mail.google.com/mail/u/0/#inbox/{message_id}"

        summary = summarize_email(email["body"])
        digest_html.append(
            f"<h3><a href='{gmail_link}' style='text-decoration: none; color: #1a73e8;'>{subject}</a> <span style='font-weight:normal;'>({sender})</span></h3>"
        )
        digest_html.append(
            f"<ul style='list-style-type: none; padding-left: 0;'>"
            + "".join(
                f"<li>{line.strip()}</li>"
                for line in summary.split("\n")
                if line.strip()
            )
            + "</ul>"
        )

    digest_html = "\n".join(digest_html)
    message = {
        "to_email": "chasegalatro@gmail.com",
        "subject": "Today's Newsletter Digest",
        "html_content": digest_html,
    }
    send_digest_email(service, **message)
    print("Digest sent!")

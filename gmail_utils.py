from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from update_token_secret import update_token_secret
from format_helpers import extract_text_from_html, extract_body_from_parts
import os
import base64

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        print(f"🔐 Loaded token.json")
        print(f"🔄 Refresh token exists? {'Yes' if creds.refresh_token else 'No'}")
        if creds.valid:
            print(f"✅ Token valid")
        else:
            print(f"⚠️ Token expired")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Attempting token refresh...")
            creds.refresh(Request())
            print("✅ Token refresh succeeded.")
        else:
            print("🧾 Starting new auth flow...")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(
                port=0, access_type="offline", prompt="consent"
            )
            print("✅ New creds acquired via consent flow.")

        # Decide how to persist token.json
        if os.getenv("GITHUB_ACTIONS") == "true":
            print("🏗 Detected GitHub Actions environment - uploading to GitHub Secret")
            try:
                update_token_secret()
                print("✅ Updated token secret")
            except Exception as e:
                print(f"❌ Failed to update GitHub secret: {e}")
        else:
            print("💾 Writing token.json locally")
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                print("✅ token.json updated")

    return build("gmail", "v1", credentials=creds)


def fetch_unread_newsletters(service, mark_as_read=False):
    query = "label:Newsletters is:unread"
    results = (
        service.users().messages().list(userId="me", q=query, maxResults=50).execute()
    )
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_id = msg["id"]
        msg_detail = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )
        payload = msg_detail.get("payload", {})
        headers = payload.get("headers", [])
        parts = payload.get("parts", [])

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "No subject"
        )
        sender = next(
            (h["value"] for h in headers if h["name"] == "From"), "Unknown sender"
        )

        # Check if this is a Morning Brew email
        is_morning_brew = "morningbrew.com" in sender.lower()

        # Extract body using different strategies
        body = ""
        if is_morning_brew:
            # For Morning Brew, use snippet to avoid scrambled content
            body = msg_detail.get("snippet", "")
        else:
            # For other emails, try full body extraction
            if parts:
                body = extract_body_from_parts(parts)

            # If no body found in parts, try the main payload
            if not body:
                data = payload.get("body", {}).get("data", "")
                if data:
                    try:
                        decoded = base64.urlsafe_b64decode(data).decode(
                            "utf-8", errors="ignore"
                        )
                        mime_type = payload.get("mimeType", "")
                        if mime_type == "text/plain":
                            body = decoded
                        elif mime_type == "text/html":
                            body = extract_text_from_html(decoded)
                    except Exception:
                        pass

            # Final fallback to snippet
            if not body:
                body = msg_detail.get("snippet", "")

        emails.append(
            {
                "subject": subject,
                "from": sender,
                "body": body,
                "message_id": msg_id,
                "thread_id": msg_detail.get("threadId", ""),
            }
        )

        if mark_as_read:
            service.users().messages().modify(
                userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
    return emails


def send_digest_email(service, to_email, subject, html_content):
    message = MIMEText(html_content, "html")
    message["to"] = to_email
    message["from"] = to_email
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}
    sent_message = service.users().messages().send(userId="me", body=body).execute()
    return sent_message

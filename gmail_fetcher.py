from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def fetch_yesterdays_newsletters(service):
    yesterday = datetime.utcnow() - timedelta(days=1)
    after = yesterday.strftime("%Y/%m/%d")
    before = (yesterday + timedelta(days=1)).strftime("%Y/%m/%d")
    query = f"label:Newsletters after:{after} before:{before}"

    results = (
        service.users().messages().list(userId="me", q=query, maxResults=50).execute()
    )

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_detail = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"], format="full")
            .execute()
        )
        payload = msg_detail.get("payload", {})
        parts = payload.get("parts", [])
        body = ""

        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )
                    break

        if not body:
            body = msg_detail.get("snippet", "")

        emails.append(body)

    return emails

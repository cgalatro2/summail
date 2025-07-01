import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

client = OpenAI()

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('gmail_client_id.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_recent_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        # Get the body or snippet
        snippet = msg_detail.get('snippet')
        emails.append(snippet)
    return emails

def summarize_email(text):
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You summarize newsletters into 3 bullet points."},
            {"role": "user", "content": f"Summarize this newsletter:\n\n{text}"}
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    service = get_gmail_service()
    emails = fetch_recent_emails(service)
    
    for i, email_text in enumerate(emails):
        print(f"\n=== Summary for email {i + 1} ===")
        summary = summarize_email(email_text)
        print(summary)

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def main():
    service = get_service()
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        print("No unread messages found.")
    else:
        print(f"Marking {len(messages)} messages as read.")
        for message in messages:
            # Mark them as read
            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    main()

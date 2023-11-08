from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import time

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

import time

def main():
    service = get_service()

    # Start with an empty page token
    page_token = None
    total_marked = 0
    request_count = 0  # Keep track of the number of API requests made

    while True:
        try:
            # Call the Gmail API to fetch INBOX
            results = service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                q="is:unread",
                pageToken=page_token
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                print("No more unread messages found.")
                break
            else:
                print(f"Retrieved {len(messages)} messages in page {request_count + 1}. Marking messages as read...")
                total_marked += len(messages)
                for message in messages:
                    # Mark them as read
                    service.users().messages().modify(
                        userId='me', 
                        id=message['id'], 
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                    print(f"Message {message['id']} marked as read.")
                
                # Increment the request count
                request_count += 1
                print(f"Finished page {request_count}. Total messages marked as read so far: {total_marked}")
            
            # Update the page token
            page_token = results.get('nextPageToken')
            if not page_token:
                print("No more pages left to process.")
                break

            # Pause for a moment to prevent hitting rate limits
            time.sleep(1)  # Sleep for 1 second; adjust as necessary based on your rate limit status
            
        except Exception as e:
            print("An error occurred:", e)
            break

    print(f"Total messages marked as read: {total_marked}")

if __name__ == '__main__':
    main()

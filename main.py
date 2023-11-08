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

def modify_message(service, user_id, message_id):
    for attempt in range(5):  # retry up to 5 times
        try:
            service.users().messages().modify(
                userId=user_id, 
                id=message_id, 
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return
        except googleapiclient.errors.HttpError as error:
            if error.resp.status in [502, 503, 504]:  # check if error is 502, 503 or 504
                time.sleep((2 ** attempt) + random.random())  # exponential backoff with jitter
            else:
                raise

def main():
    start_time = time.time()  # Record the start time

    service = get_service()

    page_token = None
    total_marked = 0
    request_count = 0

    try:
        while True:
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
                    modify_message(service, 'me', message['id'])
                
                request_count += 1
                end_time = time.time() # Record the end time
                time_spent = end_time - start_time  # Calculate the total time spent
                print(f"Finished page {request_count}. Total messages marked as read so far: {total_marked} \n Time Spent: {time_spent:.2f}")
            
            page_token = results.get('nextPageToken')
            if not page_token:
                print("No more pages left to process.")
                break

            time.sleep(1)  # Sleep for 1 second to avoid rate limits
            
    except Exception as e:
        print("An error occurred:", e)

    end_time = time.time()  # Record the end time
    time_spent = end_time - start_time  # Calculate the total time spent
    print(f"Total messages marked as read: {total_marked}")
    print(f"Total time spent: {time_spent:.2f} seconds")

if __name__ == '__main__':
    main()


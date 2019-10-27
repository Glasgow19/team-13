from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



def getLastSent():
    pastMonth = {}

    today = int(str(datetime.date(datetime.now()))[8:10])
    while today >= 1:
        pastMonth[(str(datetime.date(datetime.now()))[:8] + f"{today:02d}")] = []
        today -= 1
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)


    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    results = service.users().messages().list(userId='me', q='in:sent').execute()
    for r in results['messages']:
        r2 = service.users().messages().get(userId='me',id=r['id']).execute()
        #print(datetime.fromtimestamp(int(r2['internalDate'])/1000))
        pastMonth[str(datetime.fromtimestamp(int(r2['internalDate'])/1000))[:10]].append(str(datetime.fromtimestamp(int(r2['internalDate'])/1000))[11:])
    
    results = service.users().messages().list(userId='me', q='').execute()
    for r in results['messages']:
        r2 = service.users().messages().get(userId='me',id=r['id']).execute()
        if 'UNREAD' not in r2['labelIds']:
        #print(datetime.fromtimestamp(int(r2['internalDate'])/1000))
            pastMonth[str(datetime.fromtimestamp(int(r2['internalDate'])/1000))[:10]].append(str(datetime.fromtimestamp(int(r2['internalDate'])/1000))[11:])

    retArr = []
    for k,v in pastMonth.items():
        retArr.append(len(v))
    return retArr

""" if __name__ == '__main__':
    sent = getLastSent()
    for k,v in sent.items():
        print(k + ' - ' +  ', '.join(v)) """
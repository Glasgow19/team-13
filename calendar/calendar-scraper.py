from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

appointments = []
hours = (datetime.datetime(2019, 10, 28, 6), datetime.datetime(2019, 10, 28, 22))

def main():
    creds = None
    # file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=30, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])


    if events:
        #print(events)

        for event in events:
            ##print(event['start'])
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_parsed = str(dateutil.parser.parse(start))
            end_parsed = str(dateutil.parser.parse(end))
            #print(parsedDate, event['summary'])

            start_parsed_split = start_parsed.split(' ')
            end_parsed_split = end_parsed.split(' ')

            date_split = start_parsed_split[0].split('-')
            year = date_split[0]
            month = date_split[1]
            day = date_split[2]

            start_time_split = start_parsed_split[1].split(':')
            start_hour = start_time_split[0]
            start_mins = start_time_split[1]

            end_time_split = end_parsed_split[1].split(':')
            end_hour = end_time_split[0]
            end_mins = end_time_split[1]

            appointments.append((datetime.datetime(int(year), int(month), int(day), int(start_hour), int(start_mins)), datetime.datetime(int(year), int(month), int(day), int(end_hour), int(end_mins))))

    
    '''
    import pytz
    tz = pytz.timezone('UTC')
    
    the_datetime = tz.localize(datetime.datetime(2019, 10, 28, 0))
    the_datetime2 = tz.localize(datetime.datetime(2019, 10, 31, 8))
    body = {
        "timeMin": the_datetime.isoformat(),
        "timeMax": the_datetime2.isoformat(),
        "timeZone": 'UTC',
        "items": [{"id": 'primary'}]
       }
    eventsResult = service.freebusy().query(body=body).execute()
    print(eventsResult)
    '''

from datetime import timedelta

'''appointments = [(datetime.datetime(2012, 5, 22, 10), datetime.datetime(2012, 5, 22, 10, 30)),
                (datetime.datetime(2012, 5, 22, 12), datetime.datetime(2012, 5, 22, 13)),
                (datetime.datetime(2012, 5, 22, 15, 30), datetime.datetime(2012, 5, 22, 17, 10))]'''


def get_slots(hours, appointments, duration=timedelta(hours=1)):
    print(appointments)
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            print("{:%H:%M} - {:%H:%M}".format(start, start + duration))
            start += duration    

if __name__ == '__main__':
    main()
    get_slots(hours, appointments)

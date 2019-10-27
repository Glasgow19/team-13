import datetime
import dateutil.parser
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np
import requests

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.readonly']

events = []
events_nice = []
hours = (datetime.datetime(2019, 10, 28, 6), datetime.datetime(2019, 10, 28, 22)) # the hours of the day at which events can be made

def main(authorization):
    """ creds = None
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

    service = build('calendar', 'v3', credentials=creds) """

    #now = datetime.datetime.utcnow().isoformat() + 'Z'
    now = datetime.datetime(2019, 10, 21, 00, 00).isoformat() + 'Z'
    then = datetime.datetime(2019, 10, 27, 00, 00).isoformat() + 'Z'

    #events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=then, singleEvents=True, orderBy='startTime').execute()
    headers = {
        'Authorization' : f"Bearer {authorization}"
    }
    events_result = requests.get(f"https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={now}&timeMax={then}&singleEvents=True&orderBy=StartTime",headers=headers).json()
    events_list = events_result.get('items', [])

    if events_list:
        for event in events_list:
            # this is horrible, needs re-written
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_parsed = str(dateutil.parser.parse(start))
            end_parsed = str(dateutil.parser.parse(end))

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

            # adds event in list to datetime format
            events.append((datetime.datetime(int(year), int(month), int(day), int(start_hour), int(start_mins)), datetime.datetime(int(year), int(month), int(day), int(end_hour), int(end_mins))))

            events_nice.append((day, start_hour, end_hour, event['summary']))


# returns free slots in the user's calendar
def get_slots(hours, events, duration=timedelta(hours=1)):
    free_slots = []
    slots = sorted([(hours[0], hours[0])] + events + [(hours[1], hours[1])])

    for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
        while (start + duration) <= end:
            time_slot = "{:%H:%M}-{:%H:%M}".format(start, start + duration)
            free_slots.append(time_slot)
            start += duration
    return free_slots


# algorithm to find excerices based on your time slot
def make_exercise_suggestion():
    pass

# creates a matrix of calendar data to be sent to the webpage
def create_calendar_matrix():
    calendar = np.zeros((17, 7), int)
    event_list = []

    for event in events_nice:
        day, start_hour, end_hour, name = event
        
        day = int(day) - 21
        start_hour = int(start_hour) - 6 # start at 6am
        end_hour = int(end_hour)

        for i in range(end_hour - (start_hour + 6)):
            event_list.append(name)
            calendar[start_hour][day] = 1
            start_hour += 1

    calendar = np.asarray(calendar).flatten()
    return list(calendar), event_list

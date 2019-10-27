import datetime
import dateutil.parser
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np

from flask import Flask, render_template, request, redirect

# setup flask
app = Flask(__name__)


SCOPES = ['https://www.googleapis.com/auth/calendar']

appointments = []
appointments_nice = []
hours = (datetime.datetime(2019, 10, 28, 6), datetime.datetime(2019, 10, 28, 22)) # the hours of the day at which appointments can be made

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

    #now = datetime.datetime.utcnow().isoformat() + 'Z'
    now = datetime.datetime(2019, 10, 21, 00, 00).isoformat() + 'Z'
    then = datetime.datetime(2019, 10, 27, 00, 00).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=then, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if events:
        for event in events:
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

            # adds appointment in list to datetime format
            appointments.append((datetime.datetime(int(year), int(month), int(day), int(start_hour), int(start_mins)), datetime.datetime(int(year), int(month), int(day), int(end_hour), int(end_mins))))

            appointments_nice.append((day, start_hour, end_hour))


# returns free slots in the user's calendar
def get_slots(hours, appointments, duration=timedelta(hours=1)):
    free_slots = []
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])

    for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
        while (start + duration) <= end:
            time_slot = "{:%H:%M}-{:%H:%M}".format(start, start + duration)
            free_slots.append(time_slot)
            start += duration
    return free_slots


# returns all 1 hour slots in a day whether they are free or not
def get_all_slots():
    return get_slots(hours, appointments) + appointments


def make_exercise_suggestion():
    pass

def create_calendar_matrix():
    calendar = np.zeros((22, 7), int)

    for appointment in appointments_nice:
        day, start_hour, end_hour = appointment
        
        day = int(day) - 21
        start_hour = int(start_hour)
        end_hour = int(end_hour)

        calendar[start_hour][day] = 1
    
    calendar = np.asarray(calendar.T).flatten()
    return list(calendar)

@app.route('/')
def calender():
	return render_template('calendar.html', slots=create_calendar_matrix())


if __name__ == "__main__":
    # start server
    main()
    get_all_slots()
    print(create_calendar_matrix())
    app.run(port=8000, debug=True)

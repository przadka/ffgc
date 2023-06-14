import datetime
import json

from flask import session
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_upcoming_events():
    # Load credentials from the session.
    credentials_dict = json.loads(session['credentials'])
    credentials = Credentials.from_authorized_user_info(credentials_dict)

    service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    return events_result.get('items', [])

def get_free_slots():
       # Load credentials from the session.
    credentials_dict = json.loads(session['credentials'])
    credentials = Credentials.from_authorized_user_info(credentials_dict)

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=credentials)

    # TODO Use local timezone.
    start_time = datetime.datetime.utcnow()
    end_time = start_time + datetime.timedelta(days=7)

    # Call the Calendar API
    print('Checking free/busy information for the coming 7 days.')   
    calendar_id = 'primary' # Check the user's primary calendar
    request = service.freebusy().query(body={
        "timeMin": start_time.isoformat() + "Z",
        "timeMax": end_time.isoformat() + "Z",
        "items": [{"id": calendar_id}]
    })
    response = request.execute()
    busy_slots = response['calendars'][calendar_id]['busy']

    # List busy slots
    # output_busy = "<ul>"
    # for busy_slot in busy_slots:
    #    start = datetime.datetime.fromisoformat(busy_slot['start'])
    #    end = datetime.datetime.fromisoformat(busy_slot['end'])
    #    output_busy += "<li>Busy from " + start.isoformat() + " to " + end.isoformat() + "</li>"
    # output_busy += "</ul>"

    # Retrieve the free time slots by finding the gaps between busy slots
    free_slots = []
    if len(busy_slots) == 0:
        # If there are no busy slots, the entire time range is free
        free_slots.append({
            'start': start_time.isoformat(),
            'end': end_time.isoformat()
        })
    else:
        # Iterate over the busy slots to identify the free time intervals
        for i in range(len(busy_slots) - 1):
            start = busy_slots[i]['end']
            end = busy_slots[i + 1]['start']
            free_slots.append({
                'start': start,
                'end': end
            })
    return free_slots

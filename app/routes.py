import datetime
import json

from flask import Blueprint, Response, current_app, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return 'Welcome to my app! <a href="/authorize">Authorize</a>' + \
    '<br><br>' + current_app.config['CLIENT_ID']

@bp.route('/authorize')
def authorize():
    flow = OAuth2WebServerFlow(client_id=current_app.config['CLIENT_ID'],
        client_secret=current_app.config['CLIENT_SECRET'],
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri='http://localhost:8080/oauth2callback',
        #approval_prompt='force',
        access_type='offline')

    auth_uri = str(flow.step1_get_authorize_url())
    return redirect(auth_uri)

from flask import Response

@bp.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')
    if code:
        # exchange the authorization code for user credentials
        flow = OAuth2WebServerFlow(current_app.config['CLIENT_ID'],
        current_app.config['CLIENT_SECRET'],
        "https://www.googleapis.com/auth/calendar")
        flow.redirect_uri = request.base_url
        try:
            credentials = flow.step2_exchange(code)
        except Exception as e:
            error_message = "Unable to get an access token because "+ str(e)
            print(error_message)
            return Response(error_message, mimetype='text/plain'), 500
        
        # store these credentials for the current user in the session
        # This stores them in a cookie, which is insecure. Update this
        # with something better if you deploy to production land

        session['credentials'] = credentials.to_json()
        return Response('Credentials have been stored in session. Check your <a href="/calendar">Events</a>', mimetype='text/html')
    return Response('Authorization code not found in request', mimetype='text/plain'), 400


@bp.route('/calendar')
def calendar():
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
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'
    else:
        eventList = ""
        for event in events:
            eventDate = event['start'].get('dateTime', event['start'].get('date'))[:10]
            eventList += '<li>' + eventDate + ' - ' + event['summary'] + '</li>'
        return 'Upcoming events:' + '<ul>' + eventList + '</ul>'

@bp.route('/free')
def free():
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
    # Print the free time slots
    output_free = "<ul>"
    for slot in free_slots:
        output_free += f"<li>Free from {slot['start']} to {slot['end']}</li>"
    output_free += "</ul>"

    return output_free
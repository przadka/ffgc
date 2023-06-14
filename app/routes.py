import datetime
import json

from flask import Blueprint, Response, current_app, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

from app import gcal

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    print(current_app.config)
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
    events = gcal.get_upcoming_events()

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
    free_slots = gcal.get_free_slots()

    # Print the free time slots
    output_free = "<ul>"
    for slot in free_slots:
        output_free += f"<li>Free from {slot['start']} to {slot['end']}</li>"
    output_free += "</ul>"

    return output_free

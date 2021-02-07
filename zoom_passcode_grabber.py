#!/usr/bin/env python

from __future__ import print_function
import datetime
import pickle
import json
import os.path
import pprint
import re
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from workflow import Workflow3, ICON_WEB, web, Variables
from workflow.util import set_config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(wf):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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
            creds = flow.run_local_server(port=0, success_message="Authentication Complete. You may close this browser window and try reactivating the workflow again.")
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #now = "2021-02-05T10:30:00Z" # for testing
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        #pp = pprint.PrettyPrinter(indent=4)
        #wf.logger.debug(pp.pformat(event))
        zoom_code = fetch_passcode(event)
        #print(event['summary'], zoom_code)
        wf.add_item(title=event['summary'],
                     subtitle=f'Copy to clipboard: {zoom_code}',
                     arg=zoom_code,
                     valid=True,
                     icon=ICON_WEB)
    wf.send_feedback()

def fetch_passcode(event):
    zoom_code = ''
    try:
        zoom_code = event['conferenceData']['entryPoints'][0]['passcode']
    except KeyError:
        try: 
            description = event['description']
            description = description.replace('\n', ' ')
            #wf.logger.debug(description)
            matched_codes = re.match(r".*[Pp]asscode[^\d]*([\d]{6})", description)
            #wf.logger.debug(f"Matched Codes: {matched_codes}")
            zoom_code = matched_codes.group(1)
        except (KeyError, AttributeError):
            zoom_code = ''
    return(zoom_code)

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from Lib import base

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    date = datetime.datetime.utcnow()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    arg= date + datetime.timedelta(days=1)
    tomorrow = arg.isoformat() + 'Z'
    print('debug::::::'+tomorrow)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(now)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if event['description'] :
            print(start, event['summary'], event['description'])
        else:
            print(start, event['summary'])


    base.main(events)

if __name__ == '__main__':
    main()

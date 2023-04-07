from __future__ import print_function

import os.path
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

path = os.getcwd()
path = path + 'client_secret_1045375334810-45e7j94fvhahf6v6315km335b6dl2q8j.apps.googleusercontent.com.json'
SERVICE_ACCOUNT_FILE = 'client_secret_1045375334810-45e7j94fvhahf6v6315km335b6dl2q8j.apps.googleusercontent.com.json'
CALENDAR_ID = 'litvinzzza1@gmail.com'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/calendar']
)

service = build('calendar', 'v3', credentials=credentials)

start_time = datetime.datetime.now(pytz.utc)
end_time = start_time + datetime.timedelta(hours=1)

event = {
    'summary': 'Example Event',
    'start': {
        'dateTime': start_time.isoformat(),
        'timeZone': 'UTC'
    },
    'end': {
        'dateTime': end_time.isoformat(),
        'timeZone': 'UTC'
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 30},
            {'method': 'email', 'minutes': 60}
        ]
    }
}

service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

print('Event added to calendar.')
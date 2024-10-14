import frontmatter
import os
import pytz
import yaml
from googleapiclient.http import MediaIoBaseDownload
from slugify import slugify
from datetime import datetime
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def authenticate_google_drive():
    SCOPES = [
              'https://www.googleapis.com/auth/drive.readonly'
            ]

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    return build('drive', 'v3', credentials=creds)


def authenticate_google_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
            ]

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    return build('calendar', 'v3', credentials=creds)


def fetch_events():
    try:
        service = authenticate_google_calendar()

        events = []
        # Define the time range for future events (from now onwards)
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        # here's all the events
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items',[])
        

        for calendar in calendars:
            print(f"Calendar Summary: {calendar['summary']}, Calendar ID: {calendar['id']}")
            # Call the Calendar API to fetch events
            events_result = service.events().list(
            calendarId=calendar['id'],
                timeMin=now,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            # Get the list of events
            events.extend(events_result.get('items', []))

        # Check if any events are found
        if not events[0]:
            print('No upcoming events found.')
            return []

        # Print the events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date')) # what is this?
            print(f"{start} - {event['summary']}")

        return events

    except HttpError as error:
        print(f"An error occurred: {error}")

def fetch_drive_attachment(attachment):
    def destination_filename(attachment):
        extension = f".{attachment['mimeType'].split('/')[-1]}"
        return slugify(attachment['title'].split(extension)[0]) + extension

    service = authenticate_google_drive()
    file_name = destination_filename(attachment)
    file_path = f"./assets/images/event_flyers/{file_name}"


    with open(file_path, 'wb') as file:
        request = service.files().get_media(fileId=attachment['fileId'])
        downloader = MediaIoBaseDownload(file, request)
        done=False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress()) * 100}%")
            
        print(f"Downloaded {file_name} to {file_path}")
    return file_path

def get_first_image_attachment(event):
    attachments = event.get('attachments', [])

    if not attachments:
        print(f"No attachments found for event {event['summary']}.")
        return None


    # Loop through attachments and find the first image
    for attachment in attachments:
        mime_type = attachment.get('mimeType', '')

        # Check if it's an image attachment (based on MIME type)
        if mime_type.startswith('image/'):
            print(f"Found image attachment: {attachment['title']}")
            return fetch_drive_attachment(attachment)



def read_event_template(path):
    with open(path) as fh:
        post = frontmatter.load(fh)
    return post

def read_event_date(date):
    timezone = pytz.timezone(date['timeZone'])
    dateTime = datetime.fromisoformat(date['dateTime']).astimezone(timezone)
    return dateTime

def event_as_post(event):

    day = read_event_date(event['start']).strftime("%Y-%m-%d")
    start_time = read_event_date(event['start']).strftime("%I:%M%p")
    end_time = read_event_date(event['end']).strftime("%I:%M%p")

    post = read_event_template('_events/no-more.md')
    post.metadata['title'] = event['summary']
    post.metadata['flyer'] = get_first_image_attachment(event)
    post.metadata['date'] = day
    post.metadata['time'] = f'{start_time} - {end_time}'
    post.metadata['orgOrBandName'] = event['organizer'].get('displayName', event['organizer']['email'])
    post.content = event.get('description', event['summary'])

    return post

# Example usage
if __name__ == '__main__':
    events = fetch_events()
    posts = [event_as_post(event) for event in events]
    for post in posts:
        if post.metadata['flyer']:
            post_path=f"./_events/{slugify(post.metadata['title'])}.html"
            with open(post_path, 'w') as f:
                f.write(frontmatter.dumps(post))

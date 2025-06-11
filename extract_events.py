import datetime 
import os.path # to check whether a file exist or not

# these are used to login to my Google account and then talk to Google Calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_google_calendar_events(state):
    
    today = datetime.datetime.utcnow().date()
    time_max = datetime.datetime.combine(today, datetime.time(23,59,59))

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    creds = None 

    if os.path.exists("token_calendar.json"):
        creds = Credentials.from_authorized_user_file("token_calendar.json", SCOPES)

    if not creds or not creds.valid: #if we dont have credentials saved or the credentials is no longer valid
        if creds and creds.expired and creds.refresh_token: #if the saved token is expired but we have refresh tokens
            creds.refresh(Request()) # refreshes the login without asking the user to log in again
        else: # if we don't have valid token and we can't refresh
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES) # starts a login process to fetch a new token
            creds = flow.run_local_server(port=0)
    

    # saves the credentials to token.json file for next run
    with open("token_calendar.json", "w") as token:
        token.write(creds.to_json())

    
    try:
        service = build(serviceName="calendar", version="v3", credentials=creds) # connecting to Google Calendar

        now = datetime.datetime.utcnow().isoformat() + "Z" # fetching current time and Z indicates UTC timee

        events_result = service.events().list(
            calendarId = "primary", 
            timeMin = now,
            timeMax = time_max.isoformat() + "Z",
            singleEvents = True,
            orderBy = "startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            print("No events found.")
            return []
        
        formatted_events = []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            if len(start) == 10:
                start = start + "T00:00:00Z"
            if len(end) == 10:
                end = end + "T00:00:00Z"

            formatted_event = {
                "title" : event["summary"],
                "start_time" : start,
                "end_time" : end,
                "description" : event.get("description", "")
            }
            formatted_events.append(formatted_event)

        state["todays_events"] = formatted_events
        return state

    except Exception as e:
        print(f"An error occured: {e}")
        state["todays_events"] = []
        return state

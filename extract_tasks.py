import datetime 
import os.path # to check whether a file exist or not

# these are used to login to my Google account and then talk to Google Calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_google_tasks():
    SCOPES = ["https://www.googleapis.com/auth/tasks"]
    creds = None

    if os.path.exists("token_task.json"):
        creds = Credentials.from_authorized_user_file("token_task.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token_task.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("tasks", "v1", credentials=creds)

        # Get the user's task lists
        tasklists_result = service.tasklists().list().execute()
        tasklists = tasklists_result.get('items', [])

        all_tasks = []

        for tasklist in tasklists:
            list_id = tasklist['id']
            tasks_result = service.tasks().list(tasklist=list_id).execute()
            tasks = tasks_result.get('items', [])

            for task in tasks:
                if 'title' in task:
                    task_info = {
                        "title": task['title'],
                        "status": task.get('status', 'needsAction'),
                        "due": task.get('due', None),
                        "notes": task.get('notes', '')
                    }
                    all_tasks.append(task_info)

        return all_tasks

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

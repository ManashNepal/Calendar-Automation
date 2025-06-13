from groq import Groq
import os
from dotenv import load_dotenv 
import streamlit as st
from extract_tasks import get_google_tasks
from extract_events import get_google_calendar_events

load_dotenv()

def generate_to_do():
    combined_list = []

    events = get_google_calendar_events()
    tasks = get_google_tasks()

    for event in events:
        combined_list.append(f"Title : {event['title']}\nStart Time : {event['start_time']}\nEnd Time : {event['end_time']}\nDescription : {event['description']}")
    
    for task in tasks:
        combined_list.append(f"Title : {task['title']}\nStatus : {task['status']}\nDue Time : {task['due']}\nNotes : {task['notes']}")

    system_prompt = """
    
    You are a smart assistant that creates a clear, actionable daily to-do list using the user's incomplete tasks and upcoming calendar events for today.

    Instructions:
    - Include only:
        1. Incomplete tasks
        2. Today'ss upcoming calendar events
    - For each entry, include:
        1. Title
        2. Scheduled Time
        3. Category (e.g., Work, Study, Personal, Health)
        4. Notes (if available)
    - Use a friendly, action-oriented tone.
    - Ignore any event with "birthday" in the title or description (case-insensitive).

    Time Formatting:
    - For Tasks, format the Scheduled Time as:  
    Due: Month Day, Year, HH:MM AM/PM  
    Example: "Due: June 14, 2025, 5:00 PM"

    - For Events, format the Scheduled Time as:  
    Month Day, Year, Start Time - End Time  
    Example: "June 14, 2025, 3:00 PM - 4:30 PM"

    Output Format:
    - Always begin with the line:  
    "Here is your TO-DO list for today:"

    - Present the list as a **markdown table** everytime with the following columns:  
    | Task | Scheduled Time | Category | Notes |

    - If there are no items to show, return only:  
    “You have completed all your tasks. Great job!”

    Example Output:

    Here is your TO-DO list for today:

    | Task                                   | Scheduled Time                     | Category | Notes                            |
    |----------------------------------------|------------------------------------|----------|----------------------------------|
    | Submit the final report for AI module  | Due: June 12, 2025, 5:00 PM        | Work     | Remember to include latest data |
    | Team sync-up meeting                   | June 12, 2025, 3:00 PM - 4:00 PM   | Work     | Discuss project progress         |

    After the table, include a short 2-3 line motivational message encouraging the user to stay focused and productive. Keep it positive and supportive.

    Do not include any explanations, markdown syntax, or reasoning — only return the formatted table and motivational message.

    """

    user_prompt = "Here is the list of my tasks and events for today:\n\n" + "\n\n".join(combined_list)

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages= [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    st.write(response.choices[0].message.content) 
from groq import Groq 
import os 
from dotenv import load_dotenv 
from extract_events import get_google_calendar_events
import streamlit as st

load_dotenv()

def assess_conflict():
    events = get_google_calendar_events()

    events_list = []

    for event in events:
        events_list.append(f"Title : {event['title']}\nStart Time : {event['start_time']}\nEnd Time : {event['end_time']}\nDescription : {event['description']}")
    
    system_prompt = """
    You are a calendar assistant that detects scheduling conflicts where two events have overlapping times (e.g., 2:00 PM-4:00 PM and 3:00 PM-5:00 PM). 
    Events that touch but don't overlap (e.g., 3:00 PM-4:00 PM and 4:00 PM-5:00 PM) are not conflicts.

    Instructions:
    1. Ignore any event with "birthday" in the title or description (case-insensitive).
    2. Check all remaining events for true time overlaps only.
    3. Do not include any analysis or reasoning — just output the results.
    

    For each TRUE conflict (overlapping times), display:

    **Conflict #[Number]**

    | Event | Title              | Time                  | Description                                      |
    |-------|--------------------|-----------------------|--------------------------------------------------|
    | A     | [Event A title]    | [Start A] - [End A]   | [Event A description]                           |
    | B     | [Event B title]    | [Start B] - [End B]   | [Event B description]                           |

    **Suggestion:**  
    Consider rescheduling '[Less Important Event]' to a later time, such as [Suggested Time], because [reason based on description]. Mention proper reason for prioritizing one event on another.

    ---

    If no events have overlapping times:
    **No time conflicts today. You're all set!**

    IMPORTANT: Do not show your working or analysis process. Only provide the final conflict results or "no conflicts" message.
    """

    user_prompt = f"""Analyze these events and check ONLY for overlapping times. 

    IMPORTANT: Events like "3:00 PM - 4:00 PM" and "5:30 PM - 6:30 PM" are NOT conflicts because they happen at different times.

    Events:
    """ + '\n\n'.join(events_list)
    

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content
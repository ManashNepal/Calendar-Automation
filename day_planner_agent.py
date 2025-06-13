import os 
from groq import Groq
from dotenv import load_dotenv
from extract_events import get_google_calendar_events
from extract_tasks import get_google_tasks
import streamlit as st

load_dotenv()

def plan_the_day():
    combined_list = []

    events = get_google_calendar_events()
    tasks = get_google_tasks()

    for event in events:
        combined_list.append(f"Title : {event['title']}\nStart Time : {event['start_time']}\nEnd Time : {event['end_time']}\nDescription : {event['description']}")
    
    for task in tasks:
        combined_list.append(f"Title : {task['title']}\nStatus : {task['status']}\nDue Time : {task['due']}\nNotes : {task['notes']}")

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = """
    You are a helpful and intelligent Planner Agent.

    You will receive a list of today's events and tasks. Each item will be in one of the following formats:

    **Events:**
    Title : <event title>  
    Start Time : <start_time>  
    End Time : <end_time>  
    Description : <description>

    **Tasks:**
    Title : <task title>  
    Status : <status>  
    Due Time : <due time or "None">  
    Notes : <priority, duration, etc.>

    Your job is to:
    - Build a full-day schedule by combining fixed-time events and flexible tasks.
    - Fixed-time events must be scheduled exactly as given.
    - Flexible tasks should be placed around the events without overlap.
    - Use notes and due time to determine task priority and time required.
    - Ignore any events related to birthdays. If the event title or description contains the word "birthday" (case-insensitive), exclude it entirely from your analysis. Focus only on the remaining events.
    - Add buffer time, short breaks, meals, and sleep to create a balanced day.
    - If events conflict, try to minimize overlap and explain it briefly in the summary.
    - Do not include any analysis, explanation, or reasoning—just return the final output as specified.

    **Output Format:**
    - Start with a clean **Markdown table**.

    When you build the table:

    - Align all columns with equal spacing so that the pipe characters '|' line up vertically.
    - Pad each column with spaces to the width of the widest content in that column.
    - Use spaces, not tabs.
    - The separator row (---) must match the column widths.

    Example:

     | Time          | Activity                      | Type   | Priority |
     |---------------|-------------------------------|--------|----------|
     | 08:00 - 08:30 | Breakfast Break               | Task   | Low      |
     | 09:00 - 11:00 | Automation Project (Part 1)   | Task   | High     |

    - End with a very **brief, simple summary**:
        + No bullet points or formatting.
        + Just 2-3 plain sentences summarizing the day's focus or reminders.

    it structured, helpful, and easy to follow.
    """

    user_prompt = "Here is the list of my tasks and events for today:\n\n" + "\n\n".join(combined_list)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    return response.choices[0].message.content


        
           
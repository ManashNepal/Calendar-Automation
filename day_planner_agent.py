import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def plan_the_day(state):
    combined_list = []

    for event in state["todays_events"]:
        combined_list.append(f"Title : {event['title']}\nStart Time : {event['start_time']}\nEnd Time : {event['end_time']}\nDescription : {event['description']}")
    
    for task in state["todays_tasks"]:
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
    - **Ignore any birthday events or all-day entries** unless they're crucial to planning without mentioning in the output.
    - Add buffer time, short breaks, meals, and sleep to create a balanced day.
    - If events conflict, try to minimize overlap and explain it briefly in the summary.

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

    state["day_plan"] = response.choices[0].message.content 

    return state

        
           
from groq import Groq 
import os 
from dotenv import load_dotenv 

def assess_conflict(state):
    events = state["todays_events"]

    events_list = []

    for event in events:
        events_list.append(f"Title : {event['title']}\nStart Time : {event['start_time']}\nEnd Time : {event['end_time']}\nDescription : {event['description']}")
    
    system_prompt = """
    You are an expert calendar assistant who checks for scheduling conflicts in a user's daily events.

    Your responsibilities:
    - Analyze a list of calendar events, each with a title, start time, end time, and description.
    - Ignore any event that includes the word "birthday" in its title or description.
    - Detect if any remaining events overlap in time.
    - If conflicts are found, list them clearly and simply.
    - Suggest which event could be moved based on its importance, using the event description to infer priority.

    Instructions:
    - Use a simple, clear, and friendly tone.
    - Use 12-hour clock format with AM/PM (e.g., 2:30 PM instead of 14:30).
    - Highlight the conflicting events with their titles and times in bullet points.
    - If a conflict exists, suggest an alternative time to move one of the events (e.g., "You might move 'School Meeting' to 5:00 PM").
    - If no conflicts are found, say something like "No time conflicts today. You're all set!"
    - Do not return JSON or technical details. Just a clean, easy-to-read message.
    - Do not mention any birthday events at all.
    """

    user_prompt = f"Below is the list of today's scheduled events. Check if there are any time conflicts among them. \n\nEvents:" + '\n\n'.join(events_list)
    

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    state["conflict_assessment"] = response.choices[0].message.content 

    return state 
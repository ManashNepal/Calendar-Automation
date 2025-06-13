import os
from groq import Groq 
from dotenv import load_dotenv
from extract_events import get_google_calendar_events
from extract_tasks import get_google_tasks

def classify_priorities():
    events = get_google_calendar_events()
    tasks = get_google_tasks()

    combined_list = []

    for event in events:
        combined_list.append(f"Type : Event\nTitle : {event['title']}\nDescription : {event['description']}")
    
    for task in tasks:
        combined_list.append(f"Type : Task\nTitle : {task['title']}\nNotes : {task['notes']}")
    
    system_prompt = """
    You are a smart assistant that classifies each calendar item (Task or Event) into one of three priority levels: High, Medium, or Low.

    Use the following criteria:
    - High Priority: Time-sensitive or very important (e.g., due today, scheduled meetings, project deadlines)
    - Medium Priority: Important but not urgent (e.g., long-term goals, study sessions)
    - Low Priority: Optional or casual (e.g., leisure activities)

    **Important:** Completely ignore any calendar item that includes the word "Birthday" in the title. Do not mention or classify those items in your output.

    For each remaining item, return the result as a Markdown table with the following columns:

    | Title | Description | Priority | Reason for Priority |

    - Return only the table (no explanation, no headers beyond the table)
    - Every row should correspond to a non-birthday calendar item
    - Do not include blank rows or irrelevant content  
    """

    user_prompt = "Classify the following calendar items:\n\n" + "\n\n".join(combined_list)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    return response.choices[0].message.content


import os
from groq import Groq 
from dotenv import load_dotenv

def classify_priorities(state):
    events = state["todays_events"]
    tasks = state["todays_tasks"]

    combined_list = []

    for event in events:
        combined_list.append(f"Type : Event\nTitle : {event['title']}\nDescription : {event['description']}")
    
    for task in tasks:
        combined_list.append(f"Type : Task\nTitle : {task['title']}\nNotes : {task['notes']}")
    
    system_prompt = """
    You are a smart assistant that classifies each calendar item (tasks and events) into one of three priority levels: High, Medium, or Low.

    Use the following criteria:
    - High Priority: Time-sensitive or very important (e.g., due today, scheduled meetings, project deadlines)
    - Medium Priority: Important but not urgent (e.g., long-term goals, study sessions)
    - Low Priority: Optional or casual (e.g., leisure activities, birthdays)

    For each item, return a structured and readable explanation with:
    - Title
    - Type (Task or Event)
    - Priority (High / Medium / Low)
    - Reason for classification

    Do not summarize all items together. Give each one a clear block with line breaks.
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

    state["priorities_classification"] = response.choices[0].message.content 

    return state


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
    You are a smart assistant that classifies each calendar item (Task or Event) into one of three priority levels: High, Medium, or Low.

    Use the following criteria:
    - High Priority: Time-sensitive or very important (e.g., due today, scheduled meetings, project deadlines)
    - Medium Priority: Important but not urgent (e.g., long-term goals, study sessions)
    - Low Priority: Optional or casual (e.g., leisure activities)

    **Important:** Completely ignore any calendar item that includes the word "Birthday" in the title. Do not mention or classify those items in your output.

    For each remaining item, return it in **Markdown format** using **bold labels** and **line breaks**, like this: Include title, description, priority and reason for priority evertime in the output like:

    **Title:** Sample Title\n
    **Description:** Description of Activity\n   
    **Priority:** High\n
    **Reason for Priority:** Brief explanation  

    Separate each item with a horizontal line (`---`) and ensure line breaks between each label using `\n` or double spaces after each line. Do **not** combine multiple labels in one line.

    Return only the formatted blocks for non-birthday items. Do not include any summary or explanation.
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


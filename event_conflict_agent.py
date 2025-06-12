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

    ## Your Responsibilities:
    - Analyze a list of calendar events, each with a title, start time, end time, and description.
    - Completely ignore any event that includes the word "birthday" in its title or description.
    - Detect if any remaining events overlap in time (conflict).
    - Display each unique conflict only once.
    - Suggest which event could be moved based on its description (infer which one is more flexible or less important).

    ## Formatting Instructions:
    - Use a clear, polite, and easy-to-read tone.
    - Use 12-hour clock format with AM/PM (e.g., 3:00 PM).
    - For each conflict, use the following structure with blank lines and indentation to improve readability:

    → Conflict #[Number]

    **Event A:**  
    **Title:** [Title A]  
    **Time:** [Start Time A] - [End Time A]

    **Event B:**  
    **Title:** [Title B]  
    **Time:** [Start Time B] - [End Time B]

    **Suggestion:**  
    You might move '[Less Important Event]' to a later time, such as [Suggested Time]. (Mention the reason too).

    ---

    ## If No Conflicts:
    If there are no conflicts, respond only with:  
    **No time conflicts today. You're all set!**

    ## Important:
    - Do not include events with “birthday” in their title or description.
    - Do not return in JSON or code block format.
    - Separate multiple conflict blocks with a line of dashes (`---`).
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
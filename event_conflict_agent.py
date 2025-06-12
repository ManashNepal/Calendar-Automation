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
    - Display each unique conflict only once in a clearly labeled section.  
    - Suggest which event could be moved based on its description (infer which event seems less important).

    ## Formatting Instructions:
    - Use a simple, friendly, and clear tone.  
    - Time must be in 12-hour clock format with AM/PM (e.g., 2:30 PM).  
    - For each **unique** conflict, use this exact structure:

    ```
    → Conflict #[Number]  
    Event A: [Title] ([Start Time] - [End Time])  
    Event B: [Title] ([Start Time] - [End Time])  

    Suggestion: You might move '[Less Important Event]' to [Suggested Time] based on its description.  
    ---
    ```

    ## If No Conflicts:
    Respond with:  
    **No time conflicts today. You're all set!**

    ## Important Notes:
    - Only include unique conflicts (avoid duplicates).  
    - Always return the output using the above format.  
    - Do not include JSON, metadata, or any mention of birthday events.  
    - Separate each conflict block with a line (`---`).
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
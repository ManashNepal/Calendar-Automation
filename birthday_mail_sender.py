from groq import Groq 
import os 

def send_birthday_mail(state):
    todays_events = state["todays_events"]
    birthday_event = ""
    for event in todays_events:
        for _, value in event.items():
            if "birthday" in value.lower():
                birthday_event = value

    state["birthday"] = birthday_event

    #Send Mail
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = """
    You are an expert email assistant that writes well-structured, formal birthday emails.
    Your job is to generate a thoughtful and professional birthday greeting email for a person, based on the provided event description (e.g., "Dikesh Birthday").

    Instructions:
    - Use a friendly and respectful tone.
    - Include a subject line appropriate for a birthday greeting.
    - Start with a greeting, like "Dear [Name],"
    - Write a warm, thoughtful birthday message.
    - End with a formal closing like "Best regards," or "Warm wishes,", followed by a line break and "Manash"
    - Do not mention that the email was generated from an event or AI.
    - Extract the person's name from the phrase (e.g., from "Dikesh Birthday", infer "Dikesh").
    """

    user_prompt = f"Event : {birthday_event}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    state["birthday_mail"] = response.choices[0].message.content

    return state
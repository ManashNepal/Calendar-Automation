from groq import Groq 
import os 
from utils import parse_body, parse_subject
from dotenv import load_dotenv
from extract_events import get_google_calendar_events
import streamlit as st

load_dotenv()

def send_birthday_mail():

    return_dict = {}

    todays_events = get_google_calendar_events()
    birthday_event = ""
    for event in todays_events:
        for _, value in event.items():
            if "birthday" in value.lower():
                birthday_event = value

    #CLIENT
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    if "show_mail_editor" not in st.session_state:
        st.session_state.show_mail_editor = False 

    if "response" not in st.session_state:
        st.session_state.response = None
    
    if "birthday_message" not in st.session_state:
        st.session_state.birthday_message = ""

    user_prompt = f"Event : {birthday_event}"


    detect_birthday_prompt = """
    You are a helpful assistant that detects birthday events and responds with a short message.

    - If the event string contains a birthday, respond only in the format: "It's [Name]'s Birthday!". The name should be in Title case.
    - Extract only the name that appears immediately before the word "Birthday".
    - If there is no birthday mentioned in the event string, respond with: "No Birthday"
    - Do not add any extra information or explanation.
    """


    # respond It's [Name] Birthday -> "No Birthday" 
    detect_birthday_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : detect_birthday_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
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
    st.session_state.response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )
    # respond the generated mail
    generated_email = st.session_state.response.choices[0].message.content

    email_subject = parse_subject(generated_email)
    email_body = parse_body(generated_email)

    return_dict["email_subject"] = email_subject
    return_dict["email_body"] = email_body

    birthday_message = detect_birthday_response.choices[0].message.content
    return_dict["birthday_message"] = birthday_message

    return return_dict

    

    
      
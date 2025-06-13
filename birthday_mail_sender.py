from groq import Groq 
import os 
from utils import parse_body, parse_subject
from dotenv import load_dotenv
from extract_events import get_google_calendar_events
import streamlit as st
import yagmail

load_dotenv()

def send_birthday_mail():
    todays_events = get_google_calendar_events()
    birthday_event = ""
    for event in todays_events:
        for _, value in event.items():
            if "birthday" in value.lower():
                birthday_event = value

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

    system_prompt2 = """
    You are a helpful assistant that detects birthday events and responds with a short message: "It's [Name]'s Birthday!" using the given event string.

    - Only respond in the format: It's [Name]'s Birthday!
    - Do not add any extra information.
    - Extract only the name that appears before the word "Birthday".
    """

    # respond It's [Name] Birthday
    response2 = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt2},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    # respond generated email
    generated_email = response.choices[0].message.content

    email_subject = parse_subject(generated_email)
    email_body = parse_body(generated_email)

    st.write(response2.choices[0].message.content)

    st.write("Do you want to send the birthday mail?")
    
    if st.button("Yes", key="yes_button"):
        st.session_state.show_mail_editor = True 
    
    if "show_mail_editor" not in st.session_state:
        st.session_state.show_mail_editor = False 
    
    if st.session_state.show_mail_editor:
        st.session_state.mail = st.text_area(label= "Make changes if you have to!",value=email_body, height = 500)
        receiver_mail = st.text_input("Enter receiver email address")
        if st.button(label="SEND", key="send_button"):
            with st.spinner("Sending"):
                yag = yagmail.SMTP(user = os.getenv("SENDER_EMAIL"), password=os.getenv("APP_PASSWORD"))
                yag.send(to=receiver_mail, subject=email_subject, contents=email_body)
                st.success("Email Sent Successfully!")
    st.session_state.show_mail_editor = False
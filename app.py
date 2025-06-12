import streamlit as st 
from graphflow import graph
import yagmail 
import os


st.set_page_config(page_title="CalAutomation", page_icon=":date:")

st.header("Automate with Google Calendar :calendar:")

st.subheader("Process your Calendar before!")

if "result" not in st.session_state:
      st.session_state.result = None 

if st.button("Process", key="process_button"):
        with st.spinner("Processing..."):
            state = {}
            st.session_state.result = graph.invoke(state)
            st.success("Calendar Processes Successfully!")

user_choice = st.selectbox(label="Pick a service!", options=[
    "None",
    "Plan the Full Day", 
    "Send Birthday Mails",
    "Prioritize Task",
    "Assess Conflict",
    "Generate TO-DOs"
])

#Whole Day Planner
if user_choice == "Plan the Full Day":
      st.subheader("Click 'PLAN' to plan the whole day!")
      if st.button("PLAN", key = "plan_button"):
            st.subheader("Whole Day Plan:")
            st.write(st.session_state.result["day_plan"])

#Birthday Mail Sender
elif user_choice == "Send Birthday Mails":
    st.write(st.session_state.result["birthday_message"])

    st.write("Do you want to send the birthday mail?")
    
    if st.button("Yes", key="yes_button"):
        st.session_state.show_mail_editor = True 
    
    if "show_mail_editor" not in st.session_state:
        st.session_state.show_mail_editor = False 
    
    if st.session_state.show_mail_editor:
        st.session_state.mail = st.text_area(label= "Make changes if you have to!",value=st.session_state.result["email_body"], height = 500)
        receiver_mail = st.text_input("Enter receiver email address")
        if st.button(label="SEND", key="send_button"):
            with st.spinner("Sending"):
                yag = yagmail.SMTP(user = os.getenv("SENDER_EMAIL"), password=os.getenv("APP_PASSWORD"))
                yag.send(to=receiver_mail, subject=st.session_state.result["email_subject"], contents=st.session_state.mail)
                st.success("Email Sent Successfully!")
    st.session_state.show_mail_editor = False

elif user_choice == "Prioritize Task":
    st.subheader("Do you want to prioritize the task?")
    if st.button(label="Yes", key = "yes_button_2"):
         st.markdown(st.session_state.result["priorities_classification"], unsafe_allow_html=False)

elif user_choice == "Assess Conflict":
    st.subheader("Do you want to assess conflict in events?")
    if st.button(label="Yes", key="yes_button_3"):
         st.write(st.session_state.result["conflict_assessment"])

elif user_choice == "Generate TO-DOs":
     st.subheader("Do you want to generate To-Dos for today?")
     if st.button(label="Yes", key="yes_button_4"):
         st.write(st.session_state.result["to_do"])


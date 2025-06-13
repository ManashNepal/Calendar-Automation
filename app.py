import streamlit as st 
from day_planner_agent import plan_the_day
from birthday_mail_sender import send_birthday_mail
from priority_classifier_agent import classify_priorities
from event_conflict_agent import assess_conflict
from to_do_planner import generate_to_do
import yagmail 
import os


st.set_page_config(page_title="CalAutomation", page_icon=":date:")

st.header("Automate your Google Calendar :calendar:")

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
            with st.spinner("Planning"):
                whole_day_plan = plan_the_day()
                st.subheader("Whole Day Plan:")
                st.write(whole_day_plan)
            

#Birthday Mail Sender
elif user_choice == "Send Birthday Mails":
    with st.spinner("Loading"):
        dict = send_birthday_mail()

        #Initialized session state variables
        if "show_mail_editor" not in st.session_state:
            st.session_state.show_mail_editor = False
        
        if "edited_mail" not in st.session_state:
            st.session_state.edited_mail = ""
        
        if "receiver_mail" not in st.session_state:
            st.session_state.receiver_mail = ""

        # Check if there is any birthday
        if "No Birthday" in dict.get("birthday_message", ""):
            st.subheader("Noone has Birthday today!")

        else:
            st.write(dict["birthday_message"])

            st.write("Do you want to send the birthday mail?")
            

            if st.button("Yes", key="yes_button"):
                st.session_state.show_mail_editor = True 

            if st.session_state.show_mail_editor:
                with st.spinner("Generating Mail"):           
                    st.session_state.edited_mail = st.text_area(label= "Make changes if you have to!",value=dict["email_body"], height = 500, key="edited_mail_area")
                    st.session_state.receiver_mail = st.text_input("Enter receiver email address")

                if st.button(label="SEND", key="send_button"):
                    with st.spinner("Sending"):
                        yag = yagmail.SMTP(user = os.getenv("SENDER_EMAIL"), password=os.getenv("APP_PASSWORD"))
                        yag.send(to=st.session_state.receiver_mail, subject=dict["email_subject"], contents=st.session_state.edited_mail)
                        st.success("Email Sent Successfully!")  

                #Resetting
                st.session_state.show_mail_editor = False
                st.session_state.edited_mail = ""
                st.session_state.receiver_mail = ""  
            

# Task Prioritizing
elif user_choice == "Prioritize Task":
    st.subheader("Do you want to prioritize the task?")
    if st.button(label="Yes", key = "yes_button_2"):
        with st.spinner("Loading"):
            priorities_classification = classify_priorities()
            st.markdown(priorities_classification, unsafe_allow_html=False)

# Conflict Assessment
elif user_choice == "Assess Conflict":
    st.subheader("Do you want to assess conflict in events?")
    if st.button(label="Yes", key="yes_button_3"):
        with st.spinner("Loading"):
            conflict_assessment = assess_conflict()
            st.markdown(conflict_assessment, unsafe_allow_html=False)

# To-Dos Generation
elif user_choice == "Generate TO-DOs":
     st.subheader("Do you want to generate To-Dos for today?")
     if st.button(label="Yes", key="yes_button_4"):
        with st.spinner("Loading"):
            generate_to_do()


import streamlit as st 
from day_planner_agent import plan_the_day
from birthday_mail_sender import send_birthday_mail
from priority_classifier_agent import classify_priorities
from event_conflict_agent import assess_conflict
from to_do_planner import generate_to_do


st.set_page_config(page_title="CalAutomation", page_icon=":date:")

st.header("Automate with Google Calendar :calendar:")

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
            with st.spinner("Planning"):
                plan_the_day()
            

#Birthday Mail Sender
elif user_choice == "Send Birthday Mails":
    with st.spinner("Loading"):
         send_birthday_mail()

elif user_choice == "Prioritize Task":
    st.subheader("Do you want to prioritize the task?")
    if st.button(label="Yes", key = "yes_button_2"):
        with st.spinner("Loading"):
            priorities_classification = classify_priorities()
            st.markdown(priorities_classification, unsafe_allow_html=False)

elif user_choice == "Assess Conflict":
    st.subheader("Do you want to assess conflict in events?")
    if st.button(label="Yes", key="yes_button_3"):
        with st.spinner("Loading"):
            conflict_assessment = assess_conflict()
            st.markdown(conflict_assessment, unsafe_allow_html=False)

elif user_choice == "Generate TO-DOs":
     st.subheader("Do you want to generate To-Dos for today?")
     if st.button(label="Yes", key="yes_button_4"):
        with st.spinner("Loading"):
            generate_to_do()


from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, List
from langchain_core.runnables import RunnableLambda
from extract_events import get_google_calendar_events
from extract_tasks import get_google_tasks
from day_planner_agent import plan_the_day
from birthday_mail_sender import send_birthday_mail
from priority_classifier_agent import classify_priorities
from event_conflict_agent import assess_conflict

class Event(TypedDict):
    title : str
    start_time : str
    end_time : str
    description : str

class Task(TypedDict):
    title: str 
    status : str 
    due : str 
    notes : str 

class MyState(TypedDict):
    todays_events : Optional[List[Event]]
    todays_tasks : Optional[List[Task]]
    day_plan : Optional[str]
    email_subject : Optional[str]
    email_body : Optional[str]
    birthday_message : Optional[str]
    priorities_classification : Optional[str]
    conflict_assessment : Optional[str]

def routing_function(state):
    pass

builder = StateGraph(state_schema=MyState)

builder.add_node("Extract_Event", RunnableLambda(get_google_calendar_events))
builder.add_node("Extract_Task", RunnableLambda(get_google_tasks))
builder.add_node("Planning_Day", RunnableLambda(plan_the_day))
builder.add_node("Birthday_Mail", RunnableLambda(send_birthday_mail))
builder.add_node("Activities_Priority", RunnableLambda(classify_priorities))
builder.add_node("Conflict_Assessment", RunnableLambda(assess_conflict))

builder.add_edge(START, "Extract_Event")
builder.add_edge("Extract_Event", "Extract_Task")
builder.add_edge("Extract_Task", "Planning_Day")
builder.add_edge("Planning_Day", "Birthday_Mail")
builder.add_edge("Birthday_Mail", "Activities_Priority")
builder.add_edge("Activities_Priority", "Conflict_Assessment")
builder.add_edge("Conflict_Assessment", END)

graph = builder.compile()




from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, List
from langchain_core.runnables import RunnableLambda
from extract_events import get_google_calendar_events
from extract_tasks import get_google_tasks
from summarizer_agent import summarize_tasks
from birthday_mail_sender import send_birthday_mail
from priority_classifier_agent import classify_priorities

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
    summarized_task : Optional[str]
    is_birthday_email_sent : Optional[bool]
    priorities_classification : Optional[str]

def routing_function(state):
    pass

builder = StateGraph(state_schema=MyState)

builder.add_node("Extract_Event", RunnableLambda(get_google_calendar_events))
builder.add_node("Extract_Task", RunnableLambda(get_google_tasks))
builder.add_node("Summarize_Tasks", RunnableLambda(summarize_tasks))
builder.add_node("Birthday_Mail", RunnableLambda(send_birthday_mail))
builder.add_node("Activities_Priority", RunnableLambda(classify_priorities))

builder.add_edge(START, "Extract_Event")
builder.add_edge("Extract_Event", "Extract_Task")
builder.add_edge("Extract_Task", "Summarize_Tasks")
builder.add_edge("Summarize_Tasks", "Birthday_Mail")
builder.add_edge("Birthday_Mail", "Activities_Priority")
builder.add_edge("Activities_Priority", END)

graph = builder.compile()

state = {}

result = graph.invoke(state)

print(result)

print("\n\n---------------------")
print(result["summarized_task"])
print("\n\n---------------------")
print(result["priorities_classification"])

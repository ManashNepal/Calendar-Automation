import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def summarize_tasks(state):
    overall_task = ""
    for task in state["todays_tasks"]:
        single_task = "\n".join([f"{key} : {value}" for key, value in task.items()])
        overall_task = overall_task + "\n\n" + single_task

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = """
    You are a helpful assistant that organizes and summarizes a user's daily tasks. 
    Your job is to read through a list of tasks and generate a concise, actionable to-do list for the 
    user in a bullet-point format. Ensure clarity and include due dates or important notes if present. 
    Prioritize clarity and brevity.
    """

    user_prompt = f"""
    Here are my tasks for today:

    {overall_task}

    Please summarize these tasks into a to-do list. Use clear bullet points and combine similar tasks
    where appropriate. Include important notes or deadlines.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    state["summarized_task"] = response.choices[0].message.content 

    return state

        
           
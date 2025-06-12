from groq import Groq
import os
from dotenv import load_dotenv 

load_dotenv()

def generate_to_do(state):
    combined_list = []

    for task in state["todays_tasks"]:
        combined_list.append(f"Title : {task['title']}\nStatus : {task['status']}\nDue Time : {task['due']}\nNotes : {task['notes']}")

    system_prompt = """
    You are a helpful and intelligent task management assistant.

    Your role is to help users stay organized and productive by reviewing their current tasks and generating a concise, actionable daily to-do list. You will:

    - Analyze the user's current task list, including each task's title, status (completed/incomplete), due time, and notes.
    - Focus only on tasks that are not marked as completed.
    - Sort tasks in order of urgency, based on due time.
    - Summarize each task clearly and concisely using its title and notes.
    - If multiple tasks are due around the same time, list them in the order they appear.
    - Keep the tone friendly, but action-oriented to encourage productivity.

    Formatting Instructions:
    - Use bullet points for each to-do item, with each bullet point starting on a new line.
    - Start each task line with a verb (e.g., "Complete", "Review", "Submit", etc.).
    - Include the due time at the end in parentheses, with no extra parentheses.
    - Ensure that each bullet point is separated by a newline (i.e., \n).
    - If there are no pending tasks, simply say: “You have completed all your tasks. Great job!”

    **Follow the below Example Output. Use AM/PM format and not ISO format**

    Example output:
    • Complete the project report and send it to the manager (Due: June 12, 2025, 5:00 PM)\n
    • Review the quarterly budget spreadsheet (Due: June 13, 2025, 12:00 PM)\n
    • Submit the team feedback survey (Due: June 14, 2025, 9:00 AM)

    Do not mention any changes you made in the output.
    """

    user_prompt = "Here is the list of my tasks for today:\n\n" + "\n\n".join(combined_list)

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages= [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
    )

    state["to_do"] = response.choices[0].message.content 

    return state
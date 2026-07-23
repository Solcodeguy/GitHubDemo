# todolist.py

from datetime import datetime, date
from task import Task

def parse_due_date(due_date_str):
    try:
        return datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return None

def add_task(task_list, title, due_date=None):
    if isinstance(due_date, str):
        due_date = parse_due_date(due_date)
    task = Task(title, due_date)
    task_list.append(task)
    print("Task added successfully.")

def complete_task(task_list, index):
    try:
        task_list[index].completed = True
        print("Task marked as completed.")
    except IndexError:
        print("Error: Invalid task index.")

def delete_task(task_list, index):
    try:
        removed = task_list.pop(index)
        print(f"Deleted task: {removed.title}")
    except IndexError:
        print("Error: Invalid task index.")

def list_tasks(task_list):
    today = date.today()
    if not task_list:
        print("No tasks available.")
        return

    print("\n--- Your Tasks ---")
    for i, task in enumerate(task_list):
        overdue = ""
        if task.due_date and task.due_date < today and not task.completed:
            overdue = " **OVERDUE**"
        print(f"{i}. {task}{overdue}")


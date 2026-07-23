# main.py

import os
from todolist import add_task, complete_task, delete_task, list_tasks
from task import Task
from datetime import datetime

FILENAME = "tasks.csv"

def load_tasks():
    tasks = []
    if not os.path.exists(FILENAME):
        return tasks

    try:
        with open(FILENAME, "r") as f:
            for line in f:
                title, due_str, completed_str = line.strip().split(",")
                due_date = None
                if due_str != "None":
                    due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                completed = completed_str == "True"
                tasks.append(Task(title, due_date, completed))
    except Exception as e:
        print(f"Error loading tasks: {e}")

    return tasks

def save_tasks(task_list):
    try:
        with open(FILENAME, "w") as f:
            for task in task_list:
                due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
                f.write(f"{task.title},{due_str},{task.completed}\n")
        print("Tasks saved successfully.")
    except Exception as e:
        print(f"Error saving tasks: {e}")

def main():
    task_list = load_tasks()

    while True:
        print("\n--- To-Do Menu ---")
        print("(A) Add a new task")
        print("(C) Complete a task")
        print("(D) Delete a task")
        print("(L) List all tasks")
        print("(Q) Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "A":
            title = input("Task title: ")
            due = input("Due date (YYYY-MM-DD or leave blank): ").strip()
            due = due if due else None
            add_task(task_list, title, due)

        elif choice == "C":
            index = int(input("Task index to complete: "))
            complete_task(task_list, index)

        elif choice == "D":
            index = int(input("Task index to delete: "))
            delete_task(task_list, index)

        elif choice == "L":
            list_tasks(task_list)

        elif choice == "Q":
            save = input("Save tasks before quitting? (Y/N): ").strip().upper()
            if save == "Y":
                save_tasks(task_list)
            print("Goodbye.")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

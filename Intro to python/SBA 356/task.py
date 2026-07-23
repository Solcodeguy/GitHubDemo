# task.py
# Optional enhancement: colorama for colored output
# Install with: pip install colorama

from datetime import date

class Task:
    def __init__(self, title, due_date=None, completed=False):
        self.title = title
        self.completed = completed
        self.due_date = due_date  # either None or a date object

    def __str__(self):
        status = "[X]" if self.completed else "[-]"
        if self.due_date:
            return f"{status} {self.title} (due {self.due_date})"
        return f"{status} {self.title}"

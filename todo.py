from dotenv import load_dotenv

load_dotenv()

import os
from datetime import datetime

TODO_FILE = os.getenv("TODO_FILE")

class TaskManager:
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.isfile(self.file_path):
            open(self.file_path, 'w').close()
        self.tasks = self.load_tasks()

    def load_tasks(self):
        tasks = []
        with open(self.file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 2:
                    task, timestamp = parts
                    tasks.append((task, timestamp))
        return tasks

    def save_tasks(self):
        with open(self.file_path, 'w') as f:
            for task, timestamp in self.tasks:
                f.write(f"{task} | {timestamp}\n")

    def add_task(self, task):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tasks.append((task, timestamp))
        self.save_tasks()
        print(f"Added: '{task}' at {timestamp}")

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save_tasks()
            print(f"Removed: '{removed[0]}'")
        else:
            print("Invalid task number.")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.\n")
            return
        print("\nYour Tasks:")
        print("-" * 40)
        for i, (task, timestamp) in enumerate(self.tasks, 1):
            print(f"{i}. {task} (Added: {timestamp})")
        print("-" * 40)


def main():
    manager = TaskManager(TODO_FILE)

    while True:
        print("\n🔹 To-Do Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            manager.view_tasks()
        elif choice == '2':
            task = input("Enter new task: ").strip()
            if task:
                manager.add_task(task)
            else:
                print("Task cannot be empty.")
        elif choice == '3':
            manager.view_tasks()
            try:
                idx = int(input("Enter task number to remove: ")) - 1
                manager.remove_task(idx)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            print("Exiting. See you next time!")
            break
        else:
            print("Invalid choice. Please select from 1-4.")


if __name__ == "__main__":
    main()

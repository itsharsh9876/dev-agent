class TodoApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name):
        if len(task_name) > 0 and len(task_name) < 50:
            self.tasks.append({'name': task_name, 'done': False})
            print(f"Task '{task_name}' added successfully.")
        else:
            print("Invalid task name. Please enter a value between 1-49 characters.")

    def remove_task(self):
        if len(self.tasks) > 0:
            self.tasks.pop()
            print("Task removed successfully.")
        else:
            print("No tasks to remove.")

    def list_tasks(self):
        if len(self.tasks) > 0:
            for i, task in enumerate(self.tasks):
                status = "Done" if task['done'] else "Not Done"
                print(f"{i+1}. {task['name']} - {status}")
        else:
            print("No tasks to display.")

def main():
    todo_app = TodoApp()
    while True:
        print("\nTodo App Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            task_name = input("Enter task name: ")
            todo_app.add_task(task_name)
        elif choice == '2':
            todo_app.remove_task()
        elif choice == '3':
            todo_app.list_tasks()
        elif choice == '4':
            print("Exiting Todo App.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
class TodoApp:
    """
    A simple Todo application.

    Attributes:
        tasks (list): A list of tasks with their status.
    """

    def __init__(self):
        """
        Initializes the TodoApp instance.
        """
        self.tasks = []

    def add_task(self, task_name):
        """
        Adds a new task to the TodoApp instance.

        Args:
            task_name (str): The name of the task.

        Raises:
            ValueError: If the task name is invalid.
        """
        if len(task_name) > 0 and len(task_name) < 50:
            self.tasks.append({'name': task_name, 'done': False})
            print(f"Task '{task_name}' added successfully.")
        else:
            print("Invalid task name. Please enter a value between 1-49 characters.")

    def remove_task(self):
        """
        Removes the last task from the TodoApp instance.

        Raises:
            ValueError: If there are no tasks to remove.
        """
        if len(self.tasks) > 0:
            self.tasks.pop()
            print("Task removed successfully.")
        else:
            print("No tasks to remove.")

    def list_tasks(self):
        """
        Prints all tasks in the TodoApp instance.

        Raises:
            ValueError: If there are no tasks to display.
        """
        if len(self.tasks) > 0:
            for i, task in enumerate(self.tasks):
                status = "Done" if task['done'] else "Not Done"
                print(f"{i+1}. {task['name']} - {status}")
        else:
            print("No tasks to display.")

def main():
    """
    The main function of the TodoApp application.

    Runs an infinite loop until the user chooses to exit.
    """
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
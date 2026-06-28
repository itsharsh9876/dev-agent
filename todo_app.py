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
        # Initialize an empty list to store tasks
        self.tasks = []

    def add_task(self, task_name):
        """
        Adds a new task to the TodoApp instance.

        Args:
            task_name (str): The name of the task.

        Raises:
            ValueError: If the task name is invalid.
        """
        # Check if task name length is within valid range
        if 1 <= len(task_name) < 50:
            # Create a new task with 'done' status as False and append to tasks list
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
        # Check if tasks list is not empty
        if self.tasks:
            # Remove the last task from tasks list and print success message
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
        # Check if tasks list is not empty
        if self.tasks:
            # Iterate over each task and print its details
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
    # Create a new instance of TodoApp
    todo_app = TodoApp()
    while True:
        # Print menu options
        print("\nTodo App Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Exit")
        # Get user's choice
        choice = input("Enter your choice: ")
        if choice == '1':
            # Prompt for task name and add it to TodoApp instance
            task_name = input("Enter task name: ")
            todo_app.add_task(task_name)
        elif choice == '2':
            # Remove the last task from TodoApp instance
            todo_app.remove_task()
        elif choice == '3':
            # List all tasks in TodoApp instance
            todo_app.list_tasks()
        elif choice == '4':
            # Print exit message and break loop
            print("Exiting Todo App.")
            break
        else:
            # Handle invalid choices
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
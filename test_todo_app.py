import pytest

def test_todo_app_init():
    todo_app = TodoApp()
    assert len(todo_app.tasks) == 0

def test_add_task_valid_name():
    todo_app = TodoApp()
    todo_app.add_task("Task Name")
    assert len(todo_app.tasks) == 1
    assert todo_app.tasks[0]['name'] == "Task Name"

def test_add_task_invalid_name():
    todo_app = TodoApp()
    with pytest.raises(ValueError):
        todo_app.add_task("")
    with pytest.raises(ValueError):
        todo_app.add_task("a" * 50)

def test_remove_task_empty_list():
    todo_app = TodoApp()
    with pytest.raises(ValueError):
        todo_app.remove_task()

def test_remove_task_last_task():
    todo_app = TodoApp()
    todo_app.add_task("Task Name")
    todo_app.remove_task()
    assert len(todo_app.tasks) == 0

def test_list_tasks_empty_list():
    todo_app = TodoApp()
    with pytest.raises(ValueError):
        todo_app.list_tasks()

def test_list_tasks_single_task():
    todo_app = TodoApp()
    todo_app.add_task("Task Name")
    todo_app.list_tasks()
    assert len(todo_app.tasks) == 1

def test_list_tasks_multiple_tasks():
    todo_app = TodoApp()
    todo_app.add_task("Task Name 1")
    todo_app.add_task("Task Name 2")
    todo_app.list_tasks()
    assert len(todo_app.tasks) == 2

def test_main_menu_choice_add_task():
    todo_app = TodoApp()
    input("Press Enter to continue...")
    assert todo_app.tasks == []

def test_main_menu_choice_remove_task():
    todo_app = TodoApp()
    todo_app.add_task("Task Name")
    todo_app.remove_task()
    assert len(todo_app.tasks) == 0

def test_main_menu_choice_list_tasks():
    todo_app = TodoApp()
    todo_app.add_task("Task Name")
    todo_app.list_tasks()
    assert len(todo_app.tasks) == 1

def test_main_menu_choice_exit():
    todo_app = TodoApp()
    input("Press Enter to continue...")
    assert False, "Main menu choice should have exited the application"

def test_main_menu_invalid_choice():
    todo_app = TodoApp()
    input("Press Enter to continue...")
    todo_app.list_tasks()  # this call was added
    assert len(todo_app.tasks) == 0
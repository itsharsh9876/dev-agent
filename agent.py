import ollama
import subprocess
import os

REPO_PATH = os.getcwd()

# ── File Tools ─────────────────────────────────────────
def list_files():
    files = []
    for root, dirs, filenames in os.walk(REPO_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            rel = os.path.relpath(os.path.join(root, f), REPO_PATH)
            files.append(rel)
    return "\n".join(files)

def read_file(path):
    try:
        with open(os.path.join(REPO_PATH, path), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path, content):
    try:
        full_path = os.path.join(REPO_PATH, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written: {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True,
            capture_output=True, text=True,
            cwd=REPO_PATH
        )
        return result.stdout or result.stderr or "No output"
    except Exception as e:
        return f"Error: {e}"

# ── AI Call ────────────────────────────────────────────
def ask_ai(prompt):
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def clean_content(content):
    # Remove markdown backticks if AI adds them
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])
    return content

# ══════════════════════════════════════════════════════
# FEATURE 1: Create a New File
# ══════════════════════════════════════════════════════
def create_file_task():
    print("\n📁 CREATE A NEW FILE")
    print("-" * 40)
    files = list_files()
    task = input("What do you want to create? (e.g. Create a README.md): ")

    plan_prompt = f"""You are a coding agent working on a Git repository.
Repository files:
{files}

Task: {task}

Reply in EXACTLY this format, nothing else:
FILE_TO_CREATE: <filename>
PLAN: <one line explanation>
"""
    print("\n🧠 Thinking...")
    plan = ask_ai(plan_prompt)
    print(f"📋 Plan:\n{plan}\n")

    file_to_create = "NONE"
    for line in plan.split("\n"):
        if line.startswith("FILE_TO_CREATE:"):
            file_to_create = line.split(":", 1)[1].strip()

    if file_to_create == "NONE":
        print("❌ Could not determine file to create.")
        return

    print(f"✍️  Creating: {file_to_create}")
    create_prompt = f"""Task: {task}

Generate the complete content for: {file_to_create}

Return ONLY the file content. No explanations. No markdown backticks:"""

    content = clean_content(ask_ai(create_prompt))
    result = write_file(file_to_create, content)
    print(f"✅ {result}")
    print(f"\n📄 Preview:\n{content[:400]}\n")

# ══════════════════════════════════════════════════════
# FEATURE 2: Improve Existing File
# ══════════════════════════════════════════════════════
def improve_file_task():
    print("\n✨ IMPROVE EXISTING FILE")
    print("-" * 40)
    print(f"📁 Files in repo:\n{list_files()}\n")
    filename = input("Enter filename to improve (e.g. agent.py): ").strip()

    print(f"\n📄 Reading {filename}...")
    content = read_file(filename)

    if content.startswith("Error"):
        print(f"❌ {content}")
        return

    print("🧠 Improving code...")
    prompt = f"""Here is a Python file called {filename}:

{content}

Improve this code by:
1. Adding docstrings to all functions
2. Adding better error handling
3. Adding type hints
4. Making comments clearer
5. Improving code structure

Return ONLY the complete improved code, no explanations, no backticks:"""

    improved = clean_content(ask_ai(prompt))
    result = write_file(filename, improved)
    print(f"✅ {result}")
    print(f"\n📄 Preview of improved code:\n{improved[:400]}\n")

# ══════════════════════════════════════════════════════
# FEATURE 3: Find Bugs in a File
# ══════════════════════════════════════════════════════
def find_bugs_task():
    print("\n🐛 FIND BUGS IN A FILE")
    print("-" * 40)
    print(f"📁 Files in repo:\n{list_files()}\n")
    filename = input("Enter filename to check (e.g. agent.py): ").strip()

    print(f"\n📄 Reading {filename}...")
    content = read_file(filename)

    if content.startswith("Error"):
        print(f"❌ {content}")
        return

    print("🧠 Analyzing for bugs...")
    prompt = f"""You are a code reviewer. Analyze this code for bugs:

{content}

List ALL bugs, issues and improvements with:
- Line number (approximate)
- What the bug/issue is
- How to fix it

Be specific and thorough:"""

    result = ask_ai(prompt)
    print(f"\n🐛 Analysis Results:\n{result}\n")

# ══════════════════════════════════════════════════════
# FEATURE 4: Explain a File
# ══════════════════════════════════════════════════════
def explain_file_task():
    print("\n📖 EXPLAIN A FILE")
    print("-" * 40)
    print(f"📁 Files in repo:\n{list_files()}\n")
    filename = input("Enter filename to explain (e.g. agent.py): ").strip()

    print(f"\n📄 Reading {filename}...")
    content = read_file(filename)

    if content.startswith("Error"):
        print(f"❌ {content}")
        return

    print("🧠 Generating explanation...")
    prompt = f"""Explain this code file called {filename} in simple terms for a beginner:

{content}

Include:
1. What this file does overall
2. What each function does
3. How the code works step by step
4. Any important concepts used

Use simple language:"""

    result = ask_ai(prompt)
    print(f"\n📖 Explanation:\n{result}\n")

# ══════════════════════════════════════════════════════
# FEATURE 5: Generate Tests
# ══════════════════════════════════════════════════════
def generate_tests_task():
    print("\n🧪 GENERATE TESTS FOR A FILE")
    print("-" * 40)
    print(f"📁 Files in repo:\n{list_files()}\n")
    filename = input("Enter filename to test (e.g. agent.py): ").strip()

    print(f"\n📄 Reading {filename}...")
    content = read_file(filename)

    if content.startswith("Error"):
        print(f"❌ {content}")
        return

    print("🧠 Generating tests...")
    prompt = f"""Here is a Python file:

{content}

Generate complete pytest unit tests for all functions in this file.

Include:
- Test for normal cases
- Test for edge cases
- Test for error cases

Return ONLY the test code, no explanations, no backticks:"""

    tests = clean_content(ask_ai(prompt))
    test_filename = f"test_{filename}"
    result = write_file(test_filename, tests)
    print(f"✅ {result}")
    print(f"\n📄 Preview:\n{tests[:400]}\n")

# ══════════════════════════════════════════════════════
# FEATURE 6: Auto Commit & Push to GitHub
# ══════════════════════════════════════════════════════
def git_push_task():
    print("\n🚀 COMMIT & PUSH TO GITHUB")
    print("-" * 40)

    # Show current git status
    print("📋 Current changes:")
    status = run_command("git status --short")
    print(status)

    if not status.strip():
        print("✅ Nothing to commit - repo is clean!")
        return

    commit_msg = input("Enter commit message (or press Enter for auto-message): ").strip()

    if not commit_msg:
        # Auto generate commit message using AI
        print("🧠 Generating commit message...")
        diff = run_command("git diff --stat")
        prompt = f"""Based on these file changes, write a short git commit message (max 10 words):

{diff}

Return ONLY the commit message, nothing else:"""
        commit_msg = ask_ai(prompt).strip().replace('"', '').replace("'", "")
        print(f"📝 Auto commit message: {commit_msg}")

    print("\n⬆️  Pushing to GitHub...")
    print(run_command("git add ."))
    print(run_command(f'git commit -m "{commit_msg}"'))
    print(run_command("git push origin main"))
    print("✅ Pushed to GitHub successfully!")

# ══════════════════════════════════════════════════════
# FEATURE 7: Run Custom Task
# ══════════════════════════════════════════════════════
def custom_task():
    print("\n💬 CUSTOM TASK")
    print("-" * 40)
    files = list_files()
    task = input("Describe what you want to do: ")

    prompt = f"""You are a coding agent working on this Git repository.

Files in repo:
{files}

Task: {task}

Reply in EXACTLY this format:
FILE_TO_READ: <filename or NONE>
FILE_TO_CREATE: <filename or NONE>
COMMAND_TO_RUN: <shell command or NONE>
PLAN: <explanation>
"""
    print("\n🧠 Thinking...")
    plan = ask_ai(prompt)
    print(f"📋 Plan:\n{plan}\n")

    file_to_read = "NONE"
    file_to_create = "NONE"
    command_to_run = "NONE"

    for line in plan.split("\n"):
        if line.startswith("FILE_TO_READ:"):
            file_to_read = line.split(":", 1)[1].strip()
        elif line.startswith("FILE_TO_CREATE:"):
            file_to_create = line.split(":", 1)[1].strip()
        elif line.startswith("COMMAND_TO_RUN:"):
            command_to_run = line.split(":", 1)[1].strip()

    existing_content = ""
    if file_to_read != "NONE":
        print(f"📄 Reading: {file_to_read}")
        existing_content = read_file(file_to_read)

    if file_to_create != "NONE":
        print(f"✍️  Creating: {file_to_create}")
        create_prompt = f"""Task: {task}
{"Existing content:\n" + existing_content if existing_content else ""}
Generate content for: {file_to_create}
Return ONLY the file content, no backticks:"""
        content = clean_content(ask_ai(create_prompt))
        print(write_file(file_to_create, content))

    if command_to_run != "NONE":
        print(f"💻 Running: {command_to_run}")
        print(run_command(command_to_run))

    print("\n✅ Done!")

# ══════════════════════════════════════════════════════
# MAIN MENU
# ══════════════════════════════════════════════════════
def main():
    print("\n" + "=" * 50)
    print("🤖  OLLAMA DEV AGENT  (Free & Offline)")
    print("=" * 50)
    print(f"📂 Repo: {REPO_PATH}")
    print(f"📁 Files: {list_files()}")
    print("=" * 50)

    while True:
        print("\nWhat do you want to do?\n")
        print("  1. 📁 Create a new file")
        print("  2. ✨ Improve existing file")
        print("  3. 🐛 Find bugs in a file")
        print("  4. 📖 Explain a file")
        print("  5. 🧪 Generate tests for a file")
        print("  6. 🚀 Commit & push to GitHub")
        print("  7. 💬 Custom task")
        print("  8. ❌ Exit")

        choice = input("\nEnter choice (1-8): ").strip()

        if choice == "1":
            create_file_task()
        elif choice == "2":
            improve_file_task()
        elif choice == "3":
            find_bugs_task()
        elif choice == "4":
            explain_file_task()
        elif choice == "5":
            generate_tests_task()
        elif choice == "6":
            git_push_task()
        elif choice == "7":
            custom_task()
        elif choice == "8":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Enter 1-8.")

if __name__ == "__main__":
    main()
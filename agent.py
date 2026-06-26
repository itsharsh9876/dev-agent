import ollama
import subprocess
import os

REPO_PATH = os.getcwd()

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
        return f"Error: {e}"

def write_file(path, content):
    try:
        full_path = os.path.join(REPO_PATH, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Written: {path}"
    except Exception as e:
        return f"Error: {e}"

def ask_ai(prompt):
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

def run_agent(task):
    print(f"\n🤖 Task: {task}")
    print("=" * 50)

    files = list_files()
    print(f"📁 Repo files:\n{files}\n")

    # Step 1: Plan
    plan_prompt = f"""You are a coding agent working on a Git repository.
Repository files:
{files}

Task: {task}

Reply in EXACTLY this format, nothing else:
FILE_TO_CREATE: <filename or NONE>
PLAN: <one line explanation>
"""
    print("🧠 Thinking...")
    plan = ask_ai(plan_prompt)
    print(f"📋 Plan:\n{plan}\n")

    # Step 2: Parse
    file_to_create = "NONE"
    for line in plan.split("\n"):
        if line.startswith("FILE_TO_CREATE:"):
            file_to_create = line.split(":", 1)[1].strip()

    # Step 3: Create file
    if file_to_create != "NONE":
        print(f"✍️  Creating: {file_to_create}")

        create_prompt = f"""Task: {task}

Generate the complete content for the file: {file_to_create}

Return ONLY the file content. No explanations. No markdown backticks:"""

        content = ask_ai(create_prompt)

        # Remove backticks if AI adds them
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        result = write_file(file_to_create, content)
        print(result)
        print(f"\n📄 Preview:\n{content[:300]}")

    print("\n✅ Task Complete!")

if __name__ == "__main__":
    print("🤖 Ollama Dev Agent (Free & Offline)")
    print("=" * 50)
    task = input("Enter your task: ")
    run_agent(task)
import ollama
import subprocess
import os
import shutil
import time
from datetime import datetime

# ══════════════════════════════════════════════════════
# CONFIG - CHANGE THESE PATHS
# ══════════════════════════════════════════════════════
SOURCE_FOLDER      = "C:/Users/APNABEAST/Documents/source"       # folder to copy FROM
DESTINATION_FOLDER = "C:/Users/APNABEAST/dev-agent"              # your GitHub repo folder
REQUIREMENTS_FILE  = "C:/Users/APNABEAST/Documents/requirements.txt"  # your requirements text file
GIT_BRANCH         = "main"

# ══════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════
LOG = []

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    LOG.append(line)
    print(line)

def save_log():
    log_path = os.path.join(DESTINATION_FOLDER, "agent_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    log(f"📋 Log saved: agent_log.txt")

# ══════════════════════════════════════════════════════
# AI HELPER
# ══════════════════════════════════════════════════════
def ask_ai(prompt):
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        log(f"❌ AI Error: {e}")
        return ""

def clean_content(content):
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])
    return content.strip()

# ══════════════════════════════════════════════════════
# STEP 1: READ REQUIREMENTS FROM TEXT FILE
# ══════════════════════════════════════════════════════
def read_requirements():
    log("=" * 55)
    log("📄 STEP 1: Reading requirements file...")
    log("=" * 55)

    if not os.path.exists(REQUIREMENTS_FILE):
        log(f"❌ Requirements file not found: {REQUIREMENTS_FILE}")
        log("💡 Creating a sample requirements.txt for you...")
        sample = """# AGENT REQUIREMENTS
# Each line is a task the agent will do automatically

TRANSFER_FILES: yes
CREATE_README: yes
CREATE_GITIGNORE: yes
CREATE_REQUIREMENTS_TXT: yes
IMPROVE_CODE: yes
AUTO_COMMIT: yes
AUTO_PUSH: yes
COMMIT_MESSAGE: Auto agent - transferred files and updated repo
"""
        os.makedirs(os.path.dirname(REQUIREMENTS_FILE), exist_ok=True)
        with open(REQUIREMENTS_FILE, "w") as f:
            f.write(sample)
        log(f"✅ Sample requirements.txt created at: {REQUIREMENTS_FILE}")
        log("📝 Edit it then run agent again!")
        return None

    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    log(f"✅ Requirements loaded from: {REQUIREMENTS_FILE}")
    log(f"\n📋 Requirements content:\n{content}\n")
    return content

# ══════════════════════════════════════════════════════
# STEP 2: AI PARSES REQUIREMENTS
# ══════════════════════════════════════════════════════
def parse_requirements(req_text):
    log("=" * 55)
    log("🧠 STEP 2: AI is parsing requirements...")
    log("=" * 55)

    prompt = f"""You are an automation agent. Parse these requirements and extract tasks.

REQUIREMENTS:
{req_text}

Reply in EXACTLY this format (yes/no for each):
TRANSFER_FILES: yes or no
CREATE_README: yes or no
CREATE_GITIGNORE: yes or no
CREATE_REQUIREMENTS_TXT: yes or no
IMPROVE_CODE: yes or no
AUTO_COMMIT: yes or no
AUTO_PUSH: yes or no
COMMIT_MESSAGE: <the commit message to use>
EXTRA_TASKS: <any other tasks mentioned, or NONE>
"""
    result = ask_ai(prompt)
    log(f"📋 Parsed tasks:\n{result}\n")

    # Parse into dict
    tasks = {
        "TRANSFER_FILES": False,
        "CREATE_README": False,
        "CREATE_GITIGNORE": False,
        "CREATE_REQUIREMENTS_TXT": False,
        "IMPROVE_CODE": False,
        "AUTO_COMMIT": False,
        "AUTO_PUSH": False,
        "COMMIT_MESSAGE": "Auto agent commit",
        "EXTRA_TASKS": "NONE"
    }

    for line in result.split("\n"):
        for key in tasks:
            if line.startswith(f"{key}:"):
                val = line.split(":", 1)[1].strip()
                if key in ["TRANSFER_FILES","CREATE_README","CREATE_GITIGNORE",
                           "CREATE_REQUIREMENTS_TXT","IMPROVE_CODE","AUTO_COMMIT","AUTO_PUSH"]:
                    tasks[key] = "yes" in val.lower()
                else:
                    tasks[key] = val

    log("✅ Requirements parsed successfully!")
    return tasks

# ══════════════════════════════════════════════════════
# STEP 3: TRANSFER FILES FROM SOURCE TO DESTINATION
# ══════════════════════════════════════════════════════
def transfer_files():
    log("=" * 55)
    log("📂 STEP 3: Transferring files...")
    log("=" * 55)

    if not os.path.exists(SOURCE_FOLDER):
        log(f"⚠️  Source folder not found: {SOURCE_FOLDER}")
        log("💡 Creating sample source folder with test files...")
        os.makedirs(SOURCE_FOLDER, exist_ok=True)

        # Create sample files in source folder
        sample_files = {
            "main.py": '# Main application file\n\ndef hello():\n    print("Hello from dev agent!")\n\nif __name__ == "__main__":\n    hello()\n',
            "utils.py": '# Utility functions\n\ndef add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n',
            "config.py": '# Configuration\nAPP_NAME = "Dev Agent"\nVERSION = "1.0.0"\nDEBUG = False\n',
        }
        for filename, content in sample_files.items():
            path = os.path.join(SOURCE_FOLDER, filename)
            with open(path, "w") as f:
                f.write(content)
            log(f"   📄 Created sample: {filename}")

        log(f"✅ Sample files created in: {SOURCE_FOLDER}")

    # Make sure destination exists
    os.makedirs(DESTINATION_FOLDER, exist_ok=True)

    # Get all files from source
    transferred = []
    skipped = []

    for root, dirs, files in os.walk(SOURCE_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, SOURCE_FOLDER)
            dst_path = os.path.join(DESTINATION_FOLDER, rel_path)

            # Create subdirectories if needed
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            try:
                shutil.copy2(src_path, dst_path)
                transferred.append(rel_path)
                log(f"   ✅ Transferred: {rel_path}")
            except Exception as e:
                skipped.append(rel_path)
                log(f"   ❌ Skipped: {rel_path} ({e})")

    log(f"\n📊 Transfer Summary:")
    log(f"   ✅ Transferred: {len(transferred)} files")
    log(f"   ❌ Skipped:     {len(skipped)} files")
    return transferred

# ══════════════════════════════════════════════════════
# STEP 4: AI GENERATES FILES BASED ON REQUIREMENTS
# ══════════════════════════════════════════════════════
def list_repo_files():
    files = []
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            rel = os.path.relpath(os.path.join(root, f), DESTINATION_FOLDER)
            files.append(rel)
    return "\n".join(files)

def write_to_repo(filename, content):
    path = os.path.join(DESTINATION_FOLDER, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"   ✅ Created: {filename}")

def create_readme():
    log("\n📝 Creating README.md...")
    files = list_repo_files()
    prompt = f"""Create a professional README.md for a GitHub repository.

Files in the repo:
{files}

Include:
- Project title and description
- Features list
- Installation steps
- Usage examples
- Requirements
- License section

Return ONLY the markdown content, no backticks:"""

    content = clean_content(ask_ai(prompt))
    write_to_repo("README.md", content)

def create_gitignore():
    log("\n🚫 Creating .gitignore...")
    prompt = """Create a .gitignore file for a Python project.
Include ignores for: __pycache__, .env, venv, .pyc, logs, IDE files, OS files.
Return ONLY the .gitignore content, no explanations:"""

    content = clean_content(ask_ai(prompt))
    write_to_repo(".gitignore", content)

def create_requirements_txt():
    log("\n📦 Creating requirements.txt...")
    files = list_repo_files()

    # Read all python files to detect imports
    imports_found = []
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.endswith(".py"):
                try:
                    with open(os.path.join(root, f), "r") as fp:
                        for line in fp:
                            if line.startswith("import ") or line.startswith("from "):
                                imports_found.append(line.strip())
                except:
                    pass

    prompt = f"""Based on these Python imports found in the project:
{chr(10).join(imports_found[:30])}

Create a requirements.txt with only the third-party packages (not built-in Python modules).
Include version numbers where important.
Return ONLY the requirements.txt content:"""

    content = clean_content(ask_ai(prompt))
    write_to_repo("requirements.txt", content)

def improve_code():
    log("\n✨ Improving Python files...")
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if filename.endswith(".py") and filename != "agent.py":
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code = f.read()

                    if len(code.strip()) < 10:
                        continue

                    log(f"   🔧 Improving: {filename}")
                    prompt = f"""Improve this Python file by adding docstrings and comments:

{code}

Return ONLY the improved code, no backticks, no explanations:"""

                    improved = clean_content(ask_ai(prompt))
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(improved)
                    log(f"   ✅ Improved: {filename}")
                    time.sleep(1)  # avoid overwhelming AI
                except Exception as e:
                    log(f"   ❌ Could not improve {filename}: {e}")

# ══════════════════════════════════════════════════════
# STEP 5: GIT COMMIT & PUSH
# ══════════════════════════════════════════════════════
def run_git(command):
    result = subprocess.run(
        command, shell=True,
        capture_output=True, text=True,
        cwd=DESTINATION_FOLDER
    )
    output = result.stdout or result.stderr or ""
    return output.strip()

def git_commit_and_push(commit_message):
    log("=" * 55)
    log("🚀 STEP 5: Git commit & push...")
    log("=" * 55)

    # Check if git repo exists
    if not os.path.exists(os.path.join(DESTINATION_FOLDER, ".git")):
        log("⚠️  Not a git repo. Initializing...")
        log(run_git("git init"))
        log(run_git(f"git checkout -b {GIT_BRANCH}"))

    # Git status
    status = run_git("git status --short")
    log(f"\n📋 Changed files:\n{status}\n")

    if not status.strip():
        log("✅ Nothing to commit - everything is up to date!")
        return

    # Stage all files
    log("📦 Staging all files...")
    log(run_git("git add ."))

    # Commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{commit_message} [{timestamp}]"
    log(f"💾 Committing: {full_message}")
    commit_result = run_git(f'git commit -m "{full_message}"')
    log(commit_result)

    # Push
    log(f"⬆️  Pushing to GitHub ({GIT_BRANCH})...")
    push_result = run_git(f"git push origin {GIT_BRANCH}")
    log(push_result)

    if "error" in push_result.lower() or "fatal" in push_result.lower():
        log("❌ Push failed! Check your GitHub connection.")
        log("💡 Try: git push --set-upstream origin main")
    else:
        log("✅ Successfully pushed to GitHub!")

# ══════════════════════════════════════════════════════
# MASTER AGENT - RUNS EVERYTHING
# ══════════════════════════════════════════════════════
def run_full_agent():
    start_time = time.time()

    print("\n" + "🤖" * 25)
    print("   FULL AUTOMATED DEV AGENT")
    print("🤖" * 25)
    print(f"📂 Source:      {SOURCE_FOLDER}")
    print(f"📂 Destination: {DESTINATION_FOLDER}")
    print(f"📄 Requirements:{REQUIREMENTS_FILE}")
    print("🤖" * 25 + "\n")

    # ── STEP 1: Read requirements ──
    req_text = read_requirements()
    if req_text is None:
        log("⚠️  Created sample requirements.txt. Edit it and run again.")
        return

    # ── STEP 2: Parse requirements ──
    tasks = parse_requirements(req_text)

    # ── STEP 3: Transfer files ──
    if tasks["TRANSFER_FILES"]:
        transferred = transfer_files()
    else:
        log("⏭️  Skipping file transfer (not in requirements)")

    # ── STEP 4: Generate files ──
    log("=" * 55)
    log("✨ STEP 4: Generating files from requirements...")
    log("=" * 55)

    if tasks["CREATE_README"]:
        create_readme()
    else:
        log("⏭️  Skipping README (not in requirements)")

    if tasks["CREATE_GITIGNORE"]:
        create_gitignore()
    else:
        log("⏭️  Skipping .gitignore (not in requirements)")

    if tasks["CREATE_REQUIREMENTS_TXT"]:
        create_requirements_txt()
    else:
        log("⏭️  Skipping requirements.txt (not in requirements)")

    if tasks["IMPROVE_CODE"]:
        improve_code()
    else:
        log("⏭️  Skipping code improvement (not in requirements)")

    # ── STEP 5: Git commit & push ──
    if tasks["AUTO_COMMIT"] or tasks["AUTO_PUSH"]:
        git_commit_and_push(tasks["COMMIT_MESSAGE"])
    else:
        log("⏭️  Skipping git push (not in requirements)")

    # ── DONE ──
    elapsed = round(time.time() - start_time, 2)
    log("\n" + "=" * 55)
    log(f"✅ ALL TASKS COMPLETE in {elapsed} seconds!")
    log("=" * 55)

    save_log()

    print(f"\n🎉 Check your GitHub repo:")
    print(f"   https://github.com/itsharsh9876/dev-agent")

# ══════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    run_full_agent()
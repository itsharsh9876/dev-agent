import ollama
import subprocess
import os
import shutil
import time
import ast
import re
from datetime import datetime

# ══════════════════════════════════════════════════════
# CONFIG - CHANGE THESE PATHS
# ══════════════════════════════════════════════════════
SOURCE_FOLDER      = "C:/Users/APNABEAST/Documents/source"
DESTINATION_FOLDER = "C:/Users/APNABEAST/dev-agent"
REQUIREMENTS_FILE  = "C:/Users/APNABEAST/Documents/requirements.txt"
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
# GIT HELPERS
# ══════════════════════════════════════════════════════
def run_git(command):
    result = subprocess.run(
        command, shell=True,
        capture_output=True, text=True,
        cwd=DESTINATION_FOLDER
    )
    return (result.stdout or result.stderr or "").strip()

def git_commit(message):
    status = run_git("git status --short")
    if not status.strip():
        log(f"   ⚠️  Nothing to commit for: {message}")
        return False
    run_git("git add .")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = run_git(f'git commit -m "{message} [{timestamp}]"')
    log(f"   💾 Committed: {message}")
    log(f"   {result.splitlines()[0] if result else ''}")
    return True

def git_push():
    log("⬆️  Pushing all commits to GitHub...")
    result = run_git(f"git push origin {GIT_BRANCH}")
    log(result)
    if "error" in result.lower() or "fatal" in result.lower():
        log("❌ Push failed! Try: git push --set-upstream origin main")
    else:
        log("✅ All commits pushed to GitHub successfully!")

# ══════════════════════════════════════════════════════
# FILE TOOLS
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

# ══════════════════════════════════════════════════════
# STEP 1: READ REQUIREMENTS
# ══════════════════════════════════════════════════════
def read_requirements():
    log("=" * 55)
    log("📄 STEP 1: Reading requirements file...")
    log("=" * 55)
    if not os.path.exists(REQUIREMENTS_FILE):
        log(f"❌ Not found: {REQUIREMENTS_FILE}")
        return None
    with open(REQUIREMENTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    log(f"✅ Loaded successfully!")
    return content

# ══════════════════════════════════════════════════════
# COMMIT 1: TRANSFER FILES
# ══════════════════════════════════════════════════════
def transfer_files():
    log("=" * 55)
    log("📂 COMMIT 1: Transferring source files...")
    log("=" * 55)

    if not os.path.exists(SOURCE_FOLDER):
        log(f"⚠️  Source not found. Creating sample files...")
        os.makedirs(SOURCE_FOLDER, exist_ok=True)
        samples = {
            "main.py":    '# Main app\n\ndef hello():\n    print("Hello from dev agent!")\n\nif __name__ == "__main__":\n    hello()\n',
            "utils.py":   '# Utilities\n\ndef add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n',
            "config.py":  '# Config\nAPP_NAME = "Dev Agent"\nVERSION = "1.0.0"\nDEBUG = False\n',
            "todo_app.py":'# Todo App\ntodos = []\n\ndef add_todo(item):\n    todos.append(item)\n\ndef list_todos():\n    return todos\n\ndef remove_todo(item):\n    todos.remove(item)\n',
        }
        for fname, code in samples.items():
            with open(os.path.join(SOURCE_FOLDER, fname), "w") as f:
                f.write(code)
            log(f"   📄 Sample: {fname}")

    os.makedirs(DESTINATION_FOLDER, exist_ok=True)
    transferred = []

    for root, dirs, files in os.walk(SOURCE_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            src = os.path.join(root, filename)
            rel = os.path.relpath(src, SOURCE_FOLDER)
            dst = os.path.join(DESTINATION_FOLDER, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            transferred.append(rel)
            log(f"   ✅ Transferred: {rel}")

    log(f"\n📊 Total transferred: {len(transferred)} files")
    git_commit("feat: transfer source files to repository")
    return transferred

# ══════════════════════════════════════════════════════
# COMMIT 2: CREATE DOCUMENTATION
# ══════════════════════════════════════════════════════
def create_docs():
    log("=" * 55)
    log("📝 COMMIT 2: Creating documentation...")
    log("=" * 55)

    files = list_repo_files()

    log("\n📝 Creating README.md...")
    readme = clean_content(ask_ai(f"""Create a professional README.md for this GitHub repo.
Files: {files}
Include: title, description, features, installation, usage, license.
Return ONLY markdown, no backticks:"""))
    write_to_repo("README.md", readme)

    log("\n🚫 Creating .gitignore...")
    gitignore = clean_content(ask_ai("""Create a .gitignore for Python project.
Include: __pycache__, .env, venv, *.pyc, logs, IDE files.
Return ONLY content:"""))
    write_to_repo(".gitignore", gitignore)

    log("\n📦 Creating requirements.txt...")
    imports = []
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.endswith(".py"):
                try:
                    with open(os.path.join(root, f), "r") as fp:
                        for line in fp:
                            if line.startswith("import ") or line.startswith("from "):
                                imports.append(line.strip())
                except:
                    pass

    req = clean_content(ask_ai(f"""Based on these imports:
{chr(10).join(imports[:20])}
Create requirements.txt with only third-party packages.
Return ONLY requirements.txt content:"""))
    write_to_repo("requirements.txt", req)

    git_commit("docs: add README, .gitignore and requirements.txt")

# ══════════════════════════════════════════════════════
# COMMIT 3: IMPROVE CODE
# ══════════════════════════════════════════════════════
def improve_code():
    log("=" * 55)
    log("✨ COMMIT 3: Improving code quality...")
    log("=" * 55)

    improved = []
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if filename.endswith(".py") and filename not in ["agent.py", "agent.py"]:
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code = f.read()
                    if len(code.strip()) < 10:
                        continue
                    log(f"   🔧 Improving: {filename}")
                    better = clean_content(ask_ai(f"""Improve this Python file:
{code}
Add: docstrings, type hints, error handling, comments.
Return ONLY improved code, no backticks:"""))
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(better)
                    improved.append(filename)
                    log(f"   ✅ Improved: {filename}")
                    time.sleep(1)
                except Exception as e:
                    log(f"   ❌ Skipped {filename}: {e}")

    log(f"\n📊 Improved {len(improved)} files")
    git_commit("refactor: improve code quality, add docstrings and type hints")

# ══════════════════════════════════════════════════════
# COMMIT 4: GENERATE TESTS
# ══════════════════════════════════════════════════════
def generate_tests():
    log("=" * 55)
    log("🧪 COMMIT 4: Generating unit tests...")
    log("=" * 55)

    created = []
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if (filename.endswith(".py")
                    and not filename.startswith("test_")
                    and filename not in ["agent.py", "agent.py", "setup.py"]):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        code = f.read()
                    if "def " not in code:
                        continue
                    log(f"   🧪 Tests for: {filename}")
                    tests = clean_content(ask_ai(f"""Write pytest unit tests for:
{code}
Include: normal, edge, error cases.
Return ONLY test code, no backticks:"""))
                    write_to_repo(f"test_{filename}", tests)
                    created.append(f"test_{filename}")
                    time.sleep(1)
                except Exception as e:
                    log(f"   ❌ Skipped {filename}: {e}")

    log(f"\n📊 Created {len(created)} test files")
    git_commit("test: add pytest unit tests for all modules")

# ══════════════════════════════════════════════════════
# COMMIT 5: PERFORMANCE PROFILING REPORT
# ══════════════════════════════════════════════════════
def analyze_function_complexity(code, filename):
    """
    Statically analyzes Python code and returns metrics per function:
    - line count
    - number of loops (for/while)
    - number of nested loops
    - number of conditionals (if/elif)
    - number of function calls
    - complexity score (weighted sum)
    """
    results = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return results

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        func_name = node.name
        func_lines = (node.end_lineno - node.lineno + 1) if hasattr(node, 'end_lineno') else 0

        loops        = 0
        nested_loops = 0
        conditionals = 0
        calls        = 0
        in_loop      = False

        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                loops += 1
                # check if this loop is inside another loop
                for parent in ast.walk(node):
                    if isinstance(parent, (ast.For, ast.While)) and parent is not child:
                        for grandchild in ast.walk(parent):
                            if grandchild is child:
                                nested_loops += 1
                                break
            if isinstance(child, (ast.If, ast.IfExp)):
                conditionals += 1
            if isinstance(child, ast.Call):
                calls += 1

        # Weighted complexity score
        score = (
            func_lines * 0.1 +
            loops * 3 +
            nested_loops * 8 +
            conditionals * 2 +
            calls * 0.5
        )

        results.append({
            "file":        filename,
            "function":    func_name,
            "lines":       func_lines,
            "loops":       loops,
            "nested":      nested_loops,
            "conditions":  conditionals,
            "calls":       calls,
            "score":       round(score, 1),
        })

    return results


def performance_report():
    log("=" * 55)
    log("⚡ COMMIT 5: Performance profiling report...")
    log("=" * 55)

    all_metrics   = []
    skipped_files = []
    total_lines   = 0
    total_funcs   = 0

    # ── Collect metrics from every .py file ──
    for root, dirs, filenames in os.walk(DESTINATION_FOLDER):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()

                lines = len(code.splitlines())
                total_lines += lines

                metrics = analyze_function_complexity(code, filename)
                total_funcs += len(metrics)
                all_metrics.extend(metrics)
                log(f"   📊 Analyzed: {filename} ({lines} lines, {len(metrics)} functions)")

            except Exception as e:
                skipped_files.append(filename)
                log(f"   ⚠️  Skipped: {filename} ({e})")

    if not all_metrics:
        log("   ⚠️  No Python functions found to analyze.")
        return

    # ── Sort by complexity score descending ──
    all_metrics.sort(key=lambda x: x["score"], reverse=True)

    # ── Build the markdown table ──
    table_rows = ""
    for m in all_metrics:
        if m["score"] >= 15:
            severity = "🔴 High"
        elif m["score"] >= 7:
            severity = "🟡 Medium"
        else:
            severity = "🟢 Low"

        table_rows += (
            f"| `{m['file']}` | `{m['function']}` | {m['lines']} | "
            f"{m['loops']} | {m['nested']} | {m['conditions']} | "
            f"{m['score']} | {severity} |\n"
        )

    # ── Top 5 slowest functions for AI analysis ──
    top5 = all_metrics[:5]
    top5_summary = "\n".join(
        f"- {m['function']}() in {m['file']}: score={m['score']}, "
        f"loops={m['loops']}, nested={m['nested']}, lines={m['lines']}"
        for m in top5
    )

    log("\n🧠 AI analyzing top complex functions...")
    ai_suggestions = ask_ai(f"""You are a Python performance expert.

These are the most complex functions found by static analysis:
{top5_summary}

For each function, provide:
1. Why it might be slow
2. A specific optimization suggestion (e.g. use list comprehension, cache results, avoid nested loops)
3. Expected improvement

Format as markdown with ### headings per function. Be specific and practical:""")

    # ── Overall stats for AI ──
    avg_score = round(sum(m["score"] for m in all_metrics) / len(all_metrics), 1)
    high_risk = [m for m in all_metrics if m["score"] >= 15]
    medium_risk = [m for m in all_metrics if 7 <= m["score"] < 15]
    low_risk = [m for m in all_metrics if m["score"] < 7]

    # ── Write PERFORMANCE.md ──
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# ⚡ Performance Analysis Report

> Auto-generated by Dev Agent on {report_date}

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total files analyzed | {len(set(m['file'] for m in all_metrics))} |
| Total functions found | {total_funcs} |
| Total lines of code | {total_lines} |
| Average complexity score | {avg_score} |
| 🔴 High complexity functions | {len(high_risk)} |
| 🟡 Medium complexity functions | {len(medium_risk)} |
| 🟢 Low complexity functions | {len(low_risk)} |

---

## 🔢 Complexity Score Guide

| Score | Risk | Meaning |
|-------|------|---------|
| 0 – 6 | 🟢 Low | Simple, fast function |
| 7 – 14 | 🟡 Medium | Review for optimization |
| 15+ | 🔴 High | Likely bottleneck — optimize |

**Score formula:**
```
score = (lines × 0.1) + (loops × 3) + (nested_loops × 8) + (conditions × 2) + (calls × 0.5)
```

---

## 📋 Full Function Complexity Table

| File | Function | Lines | Loops | Nested Loops | Conditions | Score | Risk |
|------|----------|-------|-------|--------------|------------|-------|------|
{table_rows}

---

## 🧠 AI Optimization Suggestions

{ai_suggestions}

---

## 🛠️ General Performance Tips

1. **Avoid nested loops** — O(n²) complexity grows fast. Use dictionaries/sets for lookups instead.
2. **Use list comprehensions** — faster than `for` loop + `.append()`.
3. **Cache repeated results** — use `functools.lru_cache` for pure functions called multiple times.
4. **Prefer built-in functions** — `map()`, `filter()`, `sum()` are implemented in C and faster.
5. **Use generators** — `yield` instead of building large lists saves memory.
6. **Profile before optimizing** — use `cProfile` to find real bottlenecks:
   ```bash
   python -m cProfile -s cumulative your_script.py
   ```

---

## 📁 Files Skipped

{chr(10).join(f'- {f}' for f in skipped_files) if skipped_files else '- None'}

---

*Generated by [Dev Agent](https://github.com/itsharsh9876/dev-agent)*
"""

    write_to_repo("PERFORMANCE.md", content)
    log(f"\n📊 Performance Report Summary:")
    log(f"   🔴 High risk:   {len(high_risk)} functions")
    log(f"   🟡 Medium risk: {len(medium_risk)} functions")
    log(f"   🟢 Low risk:    {len(low_risk)} functions")
    log(f"   📈 Avg score:   {avg_score}")

    git_commit("perf: add performance profiling and optimization report")


# ══════════════════════════════════════════════════════
# SHOW COMMIT HISTORY
# ══════════════════════════════════════════════════════
def show_commit_history():
    log("=" * 55)
    log("📜 FINAL COMMIT HISTORY")
    log("=" * 55)
    history = run_git("git log --oneline -10")
    for line in history.splitlines():
        log(f"   {line}")

# ══════════════════════════════════════════════════════
# MASTER AGENT
# ══════════════════════════════════════════════════════
def run_full_agent():
    start_time = time.time()

    print("\n" + "🤖" * 25)
    print("   FULL AUTOMATED DEV AGENT")
    print("   4 COMMITS → AUTO PUSH")
    print("🤖" * 25)
    print(f"📂 Source:       {SOURCE_FOLDER}")
    print(f"📂 Destination:  {DESTINATION_FOLDER}")
    print(f"📄 Requirements: {REQUIREMENTS_FILE}")
    print("🤖" * 25)
    print("""
📌 COMMIT PLAN:
   COMMIT 1 → feat:     Transfer source files
   COMMIT 2 → docs:     README + .gitignore + requirements.txt
   COMMIT 3 → refactor: Improve code quality
   COMMIT 4 → test:     Add unit tests
   COMMIT 5 → perf:     Performance profiling report
   PUSH     → All commits go live on GitHub
""")

    req_text = read_requirements()
    if req_text is None:
        log("❌ Fix requirements file and try again.")
        return

    transfer_files()
    create_docs()
    improve_code()
    generate_tests()
    performance_report()

    save_log()
    git_commit("chore: add agent activity log")

    log("=" * 55)
    log("🚀 PUSHING ALL COMMITS TO GITHUB...")
    log("=" * 55)
    git_push()

    show_commit_history()

    elapsed = round(time.time() - start_time, 2)
    log(f"\n✅ ALL DONE in {elapsed} seconds!")

    print(f"""
🎉 CHECK YOUR GITHUB REPO:
   https://github.com/itsharsh9876/dev-agent

📊 YOU SHOULD SEE 6 COMMITS:
   ✅ feat:     transfer source files
   ✅ docs:     README, .gitignore, requirements
   ✅ refactor: improve code quality
   ✅ test:     add unit tests
   ✅ perf:     performance profiling report
   ✅ chore:    agent activity log
""")

if __name__ == "__main__":
    run_full_agent()
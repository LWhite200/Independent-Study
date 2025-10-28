"""
🧠 Simple Standalone Coding AI Agent
-----------------------------------
- Asks the user to pick a simple coding task.
- Generates Python code (using local AI model or fallback).
- Saves the result into data/output/code_test.py
"""

import os
import requests

# ----------------------------
# Helper: ask local AI model
# ----------------------------
def ask_ai(prompt):
    """Send prompt to local AI model or fallback if offline."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": prompt, "stream": False},
            timeout=10
        )
        return response.json().get("response", "").strip()
    except Exception:
        # Fallback (if no model running)
        return "# AI model unavailable — fallback response.\nprint('Hello from fallback!')"

# ----------------------------
# Step 1: Choose a coding task
# ----------------------------
def choose_task():
    tasks = {
        "1": "Write a Python for loop that adds the first 5 numbers (1 to 5).",
        "2": "Write a Python list comprehension that squares numbers 1 to 5.",
        "3": "Write a Python function that returns the factorial of a number.",
        "4": "Write a Python script that prints 'Hello AI Agents!'.",
        "5": "Write a Python loop that prints even numbers from 1 to 10."
    }

    print("\n🤖 Choose a coding task:")
    for k, v in tasks.items():
        print(f" {k}) {v}")

    choice = input("\nEnter task number (1–5): ").strip()
    return tasks.get(choice, tasks["1"])

# ----------------------------
# Step 2: Generate the code
# ----------------------------
def generate_code(task):
    """Ask the AI model to generate Python code for the selected task."""
    prompt = f"""You are a helpful coding assistant.
Task: {task}
Return ONLY runnable Python code. No explanations."""
    return ask_ai(prompt)

# ----------------------------
# Step 3: Save the output
# ----------------------------
def save_code(code):
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "code_test.py")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"\n✅ Code saved to {file_path}\n")
    print("--- Generated Code ---")
    print(code)

# ----------------------------
# Main flow
# ----------------------------
if __name__ == "__main__":
    print("=== Simple Coding AI Agent ===")
    task = choose_task()
    print(f"\n🧩 Selected Task:\n{task}\n")

    code = generate_code(task)
    save_code(code)

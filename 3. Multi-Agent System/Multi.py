import requests
import os
from openpyxl import Workbook

# -----------------------------
# Setup directories
# -----------------------------
DATA_DIR = "data"
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

input_file = os.path.join(INPUT_DIR, "names.txt")

# -----------------------------
# Function to talk to AI model
# -----------------------------
def ask_ai(role, prompt):
    """Send prompt to the local AI model."""
    print(f"\n[{role}] Thinking...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3", "prompt": prompt, "stream": False}
    )
    text = response.json()["response"].strip()
    print(f"[{role}] → {text}")
    return text

# -----------------------------
# Agents
# -----------------------------

def agent_cleaner(names):
    prompt = f"""
You are a data cleaner agent.
Task: Remove duplicates, trim spaces, and fix capitalization.
Return only cleaned names as comma-separated list.
Names: {', '.join(names)}
"""
    cleaned = ask_ai("🧹 Cleaner", prompt)
    return [n.strip() for n in cleaned.split(",") if n.strip()]

def agent_sorter(names):
    prompt = f"""
You are a sorting agent.
Sort these names alphabetically and return only a comma-separated list.
Names: {', '.join(names)}
"""
    sorted_result = ask_ai("🧠 Sorter", prompt)
    return [n.strip() for n in sorted_result.split(",") if n.strip()]

def agent_reporter(names):
    summary = f"Total names: {len(names)}\nFirst: {names[0]}\nLast: {names[-1]}"
    print(f"\n[📊 Reporter] Summary of results:\n{summary}")
    wb = Workbook()
    ws = wb.active
    ws.title = "Sorted Names"
    for i, name in enumerate(names, start=1):
        ws.cell(row=i, column=1, value=name)
    output_file = os.path.join(OUTPUT_DIR, "sorted_names.xlsx")
    wb.save(output_file)
    print(f"[📊 Reporter] ✅ Saved results to {output_file}")

# -----------------------------
# Coordinator
# -----------------------------
def main():
    # Read input
    with open(input_file, "r", encoding="utf-8") as f:
        raw_names = [line.strip() for line in f if line.strip()]

    print("=== MULTI-AGENT DEMO START ===")

    # Agent 1 cleans
    cleaned = agent_cleaner(raw_names)

    # Agent 2 sorts
    sorted_names = agent_sorter(cleaned)

    # Agent 3 reports
    agent_reporter(sorted_names)

    print("\n=== MULTI-AGENT DEMO COMPLETE ===")

if __name__ == "__main__":
    main()

import requests
import json
import os
from openpyxl import Workbook  # Excel writing library

# -----------------------------
# Setup parent + input/output folders
# -----------------------------
DATA_DIR = "data"
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

# Create folders if they don’t exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path to names.txt (should be inside data/input folder)
input_file = os.path.join(INPUT_DIR, "names.txt")

# -----------------------------
# Load names from file
# -----------------------------
# Each line in names.txt should contain one name.
with open(input_file, "r", encoding="utf-8") as f:
    names = [line.strip() for line in f if line.strip()]

# -----------------------------
# Function to talk to local AI model
# -----------------------------
def ask_ai(prompt):
    """
    Send a prompt to the AI model running locally on port 11434.
    Returns the model's text output (string).
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",   # model name (adjust if needed)
            "prompt": prompt,  # the sorting instruction
            "stream": False    # disable streaming, return whole response
        }
    )
    return response.json()["response"]

# -----------------------------
# Build the instruction prompt
# -----------------------------
prompt = f"""Sort these names alphabetically: {', '.join(names)}

IMPORTANT: Return ONLY a comma-separated list in correct alphabetical order.
Include ALL names exactly as given.

Names to sort: {', '.join(names)}"""

# -----------------------------
# Ask the AI to sort the names
# -----------------------------
result = ask_ai(prompt)

# Print raw AI output to terminal
print("AI Result:", result)




# -----------------------------
# Save results to Excel (or TXT fallback)
# -----------------------------
try:
    # Split the comma-separated list into individual names
    ai_list = [name.strip() for name in result.split(",") if name.strip()]

    # Create a new Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Sorted Names"

    # Write names into first column
    for i, name in enumerate(ai_list, start=1):
        ws.cell(row=i, column=1, value=name)

    # Save Excel file into output folder
    output_file = os.path.join(OUTPUT_DIR, "sorted_names.xlsx")
    wb.save(output_file)
    print(f"✅ Saved AI-sorted names to {output_file}")

except Exception as e:
    # If Excel fails, fall back to plain text file in output folder
    output_file = os.path.join(OUTPUT_DIR, "sorted_names.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Could not write Excel file, saved to {output_file} instead. Error: {e}")
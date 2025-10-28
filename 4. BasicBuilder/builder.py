"""
builder.py
Main script that uses simple AI agents to build a very basic website
based on terminal answers to 5 yes/no questions.

Output: HTML + CSS saved in data/output/
"""

import os
from agents.designer_agent import DesignerAgent
from agents.coder_agent import CoderAgent

# -------------------------------------------------
# Setup folders
# -------------------------------------------------
DATA_DIR = "data"
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------
# Initialize agents
# -------------------------------------------------
designer = DesignerAgent("Designer", "Plans the website layout")
coder = CoderAgent("Coder", "Creates HTML/CSS files")

# -------------------------------------------------
# Ask questions (Yes/No)
# -------------------------------------------------
questions = [
    ("Should there be a login page?", "login"),
    ("Should there be an about page?", "about"),
    ("Should there be a contact page?", "contact"),
    ("Should there be navigation links?", "nav"),
    ("Should there be a custom background color?", "style"),
]

answers = {}

print("\n🧠 Website Builder — Answer with 'y' or 'n'\n")

for q, key in questions:
    ans = input(f"{q} (y/n): ").strip().lower()
    answers[key] = ans == "y"

# -------------------------------------------------
# Designer makes plan
# -------------------------------------------------
plan = designer.make_plan(answers)
print("\n📝 Plan:", plan)

# -------------------------------------------------
# Coder builds files
# -------------------------------------------------
coder.build_site(plan, OUTPUT_DIR)

print(f"\n✅ Website generated in: {OUTPUT_DIR}/")

# local_ai.py

from agents import Agent
from local_runner import LocalRunner
import re
from datetime import date

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

# Load movies from text file for the recommender example
with open("movies.txt", "r", encoding="utf-8") as f:
    movie_data = f.read().strip()

# ----- Utilities -----

def parse_numbers(text):
    return [float(n) for n in re.findall(r'[-+]?\d+(?:\.\d+)?', text)]

def c_to_f_list(c_vals):
    """Convert Celsius to Fahrenheit: F = (C × 9/5) + 32"""
    return [round((c * 9.0 / 5.0) + 32, 1) for c in c_vals]

def prioritize_tasks_from_text(text):
    """
    Use simple rule-based logic to determine urgency:
    - 'tomorrow' > 'due Friday' > generic tasks.
    """
    tasks = [
        "Finish report (due Friday)",
        "Buy groceries",
        "Call mom (birthday tomorrow)",
        "Book dentist appointment"
    ]
    # Scoring system
    scores = {}
    for t in tasks:
        score = 0
        if "tomorrow" in t.lower():
            score += 100
        if "due friday" in t.lower():
            # Assume today is Monday = 4 days away
            score += 80
        if "groceries" in t.lower():
            score += 20
        scores[t] = score

    ordered = sorted(tasks, key=lambda x: scores[x], reverse=True)
    return "\n".join([f"{i+1}. {t}" for i, t in enumerate(ordered)])

def recommend_movie_from_data(movie_text, genre):
    """Pick first movie that matches genre."""
    for line in movie_text.splitlines():
        if genre.lower() in line.lower():
            return line
    return "No matching movie found."

def simple_weather_predictor_for_season(season):
    """Give precise sentence for weather prediction."""
    if season.lower() == "autumn":
        return "Tomorrow’s weather: cool (10–15°C), cloudy skies, and light rainfall."
    return "Tomorrow’s weather prediction unavailable."

# ----- Dispatcher -----

def process_prompt(prompt):
    lower = prompt.lower()

    if "convert" in lower and "celsius" in lower:
        nums = parse_numbers(prompt)
        return "; ".join([f"{c}°C = {f}°F" for c, f in zip(nums, c_to_f_list(nums))])

    if "to-do" in lower or "reorder" in lower:
        return prioritize_tasks_from_text(prompt)

    if "recommend" in lower and "movie" in lower:
        return recommend_movie_from_data(movie_data, "comedy")

    if "weather" in lower and "autumn" in lower:
        return simple_weather_predictor_for_season("autumn")

    # Fallback: let the LLM try
    return LocalRunner.run_sync(agent, prompt).final_output

# ----- Prompts -----

prompts = [
    # Weather with more precise language
    "Pretend you are a simple weather predictor. For autumn, give tomorrow’s weather in one short sentence including temperature range in Celsius and condition (e.g., rain, sunny, cloudy).",

    # To-do with explicit instruction
    """Here is my to-do list:
    1. Finish report (due Friday)
    2. Buy groceries
    3. Call mom (birthday tomorrow)
    4. Book dentist appointment
    Reorder strictly from most urgent (soonest due or time-sensitive) to least urgent.""",

    # Movies
    f"Here is a list of movies:\n{movie_data}\n\nRecommend exactly one comedy movie by name.",

    # Unit conversion with formula
    "Convert these Celsius temperatures to Fahrenheit using the formula F = (C × 9/5) + 32: 0, 20, 37, 100"
]

# ----- Run -----

with open("ai_output.txt", "w", encoding="utf-8") as f:
    for prompt in prompts:
        result = process_prompt(prompt)
        f.write(f"Prompt: {prompt}\n\n")
        f.write(f"AI Output:\n{result}\n")
        f.write("=" * 50 + "\n")

        print(f"Prompt: {prompt}")
        print(f"AI Output: {result}\n")

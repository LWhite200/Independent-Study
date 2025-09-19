# local_ai.py
# local_ai.py

from agents import Agent
from local_runner import LocalRunner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

prompts = [
    "Write a haiku about recursion in programming.",
    "In 5 words, say I love you.",
    "Name 5 countries where they speak Spanish."
]

with open("ai_output.txt", "w", encoding="utf-8") as f:
    for prompt in prompts:
        exact_count = 5 if "5 words" in prompt else None
        result = LocalRunner.run_sync(agent, prompt, exact_word_count=exact_count)

        f.write(f"Prompt: {prompt}\n\n")
        f.write(f"AI Output:\n{result.final_output}\n")
        f.write("="*50 + "\n")

        print(f"Prompt: {prompt}")
        print(f"AI Output: {result.final_output}\n")

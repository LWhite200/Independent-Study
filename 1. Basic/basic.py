"""
🧩 SIMPLE AI AGENT BASE
A minimal guide for building small AI agents.

Each agent has:
 - instructions → what it should do
 - tools        → what functions it can use
 - guardrails   → basic safety checks
 - hooks        → places to extend behavior
"""

import requests

# -------------------------------------------------
# 🧠 Basic Agent
# -------------------------------------------------
class Agent:
    def __init__(self, name, instructions, tools=None, guardrails=None, hooks=None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or {}
        self.guardrails = guardrails or {}
        self.hooks = hooks or {}

    # -------------------------
    # Main reasoning step
    # -------------------------
    def think(self, task):
        """Talk to the AI model using the agent’s instructions."""
        prompt = f"{self.instructions}\n\nTask: {task}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": prompt, "stream": False}
        )

        return response.json().get("response", "").strip()

    # -------------------------
    # Tool usage
    # -------------------------
    def use_tool(self, tool_name, *args):
        """Run a tool the agent has permission for."""
        if tool_name in self.tools:
            return self.tools[tool_name](*args)
        else:
            raise Exception(f"{self.name} cannot use tool '{tool_name}'")

    # -------------------------
    # Guardrail check
    # -------------------------
    def check(self, rule_name, data):
        """Run a guardrail before acting."""
        if rule_name in self.guardrails:
            return self.guardrails[rule_name](data)
        return True

    # -------------------------
    # Hook (event extension)
    # -------------------------
    def run_hook(self, hook_name, *args):
        """Run optional hook (e.g., before_think, after_think)."""
        if hook_name in self.hooks:
            return self.hooks[hook_name](*args)


# -------------------------------------------------
# ⚙️ Example Usage
# -------------------------------------------------
if __name__ == "__main__":
    # Simple tool
    def count_words(text):
        return len(text.split())

    # Simple guardrail
    def no_emails(text):
        return "@" not in text

    # Simple hook
    def on_finish(result):
        print("Hook → Agent finished thinking:", result)

    # Create agent
    bot = Agent(
        name="MiniBot",
        instructions="You are a simple helper that answers briefly.",
        tools={"count_words": count_words},
        guardrails={"no_emails": no_emails},
        hooks={"after_think": on_finish}
    )

    # Example run
    task = "Say hello to the world."
    if bot.check("no_emails", task):
        result = bot.think(task)
        bot.run_hook("after_think", result)
        print("Result:", result)

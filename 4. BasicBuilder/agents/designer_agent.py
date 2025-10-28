"""
designer_agent.py
Defines a simple planning agent that decides what pages to build.
"""

class DesignerAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def make_plan(self, answers):
        """Convert yes/no answers into a simple website plan."""
        plan = {
            "include_login": answers.get("login", False),
            "include_about": answers.get("about", False),
            "include_contact": answers.get("contact", False),
            "include_nav": answers.get("nav", False),
            "use_custom_style": answers.get("style", False),
        }
        return plan

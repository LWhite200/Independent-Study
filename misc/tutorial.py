# tutorial.py
"""
Tutorial: Setting up and testing phi-3 with Ollama and Python (Windows CMD)
--------------------------------------------------------------------------

1. Install Python (3.10+ recommended)
   https://www.python.org/downloads/

2. Open Command Prompt (cmd.exe), then create and activate a virtual environment:
       python -m venv .venv
       .venv\\Scripts\\activate.bat    # backslashes escaped
       OR
       .venv/Scripts/activate.bat      # forward slashes also work in CMD
       # Please not that I already have this downloaded, so just move this file out of this folder
       # But it is still good practice to .venv\\Scripts\\activate before using the agent
       
3. Install dependencies inside the venv:
       pip install requests

4. Install Ollama:
   Download and install from → https://ollama.ai/download

5. Pull the phi-3 model with Ollama:
       ollama pull phi3

6. Run this Python file to test your setup:
       python tutorial.py
"""


import requests

def ask_ai(prompt: str) -> str:
    """
    Send a prompt to the locally running Ollama server.
    Requires Ollama running on http://localhost:11434.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",   # model name (make sure you've pulled it)
            "prompt": prompt,
            "stream": False    # disable streaming for simplicity
        }
    )
    return response.json()["response"]

# -----------------------------
# Example test prompt
# -----------------------------
result = ask_ai("Hello! Can you confirm that you are working correctly?")
print("AI Response:", result)
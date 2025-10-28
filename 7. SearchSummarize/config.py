# config.py
# Store your Gemini API key safely (don’t commit to GitHub!)
# config.py
# Store your Gemini API key safely (don’t commit to GitHub!)
import os
import google.generativeai as genai

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GEMINI_API_KEY environment variable.")
    genai.configure(api_key=api_key)

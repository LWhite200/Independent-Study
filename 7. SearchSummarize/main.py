# main.py
from config import configure_gemini
from agent import research_agent

def main():
    configure_gemini()
    print("Welcome to the Gemini Research & Summary Agent!")
    topic = input("Enter a topic to research: ").strip()
    if topic:
        research_agent(topic)
    else:
        print("No topic entered. Exiting.")

if __name__ == "__main__":
    main()

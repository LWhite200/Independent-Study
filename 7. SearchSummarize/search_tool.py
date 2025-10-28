# search_tool.py
# search_tool.py
from ddgs import DDGS

def search_topic(topic, max_results=5):
    """
    Perform a web search and return short text snippets.
    """
    print(f"🔎 Searching the web for: {topic}")
    results = DDGS().text(topic, max_results=max_results)
    snippets = [r.get("body") for r in results if r.get("body")]
    
    if not snippets:
        print("⚠️ No snippets found. Try another topic or check your connection.")
    return snippets

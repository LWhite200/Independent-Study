# agent.py
import re
from search_tool import search_topic
from summarizer import summarize_text
from rich.console import Console

console = Console()

def sanitize_filename(s):
    # Keep only the first two words
    words = s.split()[:2]
    base = "_".join(words)
    # Replace invalid Windows filename characters
    return re.sub(r'[\\/*?:"<>|]', "_", base)

def research_agent(topic):
    console.rule(f"[bold blue]Research Agent: {topic}[/bold blue]")

    """
    Complete agent pipeline:
    1. Search topic
    2. Summarize each snippet
    3. Merge into a final summary
    4. Save as markdown report
    """

    snippets = search_topic(topic)
    if not snippets:
        console.print("[red]No search results found.[/red]")
        return

    console.print(f"📄 Found {len(snippets)} snippets. Summarizing...")

    partial_summaries = []
    for i, s in enumerate(snippets, 1):
        console.print(f"\n[cyan]Summarizing snippet {i}...[/cyan]")
        summary = summarize_text(s)
        partial_summaries.append(summary)

    combined_text = "\n\n".join(partial_summaries)
    console.print("\n🧠 Combining summaries into a final report...")
    final_summary = summarize_text(combined_text)

    safe_name = sanitize_filename(topic)
    output_path = f"report_{safe_name}.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Research Report: {topic}\n\n{final_summary}")

    console.print(f"\n✅ Done! Report saved as [green]{output_path}[/green]\n")

from typing import List
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from src.milestone_1.phase_2_preferences.schema import Recommendation

# Using a path relative to this file
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

def format_as_terminal(recommendations: List[Recommendation]) -> str:
    """
    Formats recommendations for terminal output.
    """
    if not recommendations:
        return (
            "No results found matching your criteria.\n"
            "Tip: Try widening your budget or lowering your minimum rating."
        )
        
    output = ["--- AI RESTAURANT RECOMMENDATIONS ---"]
    for r in recommendations:
        output.append(f"Rank {r.rank}: {r.restaurant_name} (Rating: {r.rating}, Cost: {r.estimated_cost})")
        output.append(f"Cuisines: {', '.join(r.cuisines)}")
        output.append(f"Why this was selected: {r.explanation}")
        output.append("-" * 40)
    return "\n".join(output)

def format_as_html(recommendations: List[Recommendation]) -> str:
    """
    Formats recommendations for HTML output using Jinja2.
    """
    if not TEMPLATES_DIR.exists():
        return "Error: Templates directory not found."
        
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    try:
        template = env.get_template("results.html")
        return template.render(recommendations=recommendations)
    except Exception as e:
        return f"Error rendering HTML: {e}"

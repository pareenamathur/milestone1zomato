from typing import List
from src.milestone_1.phase_2_preferences.schema import Recommendation
from src.milestone_1.phase_5_output.formatter import format_as_terminal, format_as_html

def display_recommendations(recommendations: List[Recommendation], format_type: str = "terminal"):
    """
    Handles the final display of recommendations based on the requested format.
    """
    if format_type == "terminal":
        print(format_as_terminal(recommendations))
    elif format_type == "html":
        return format_as_html(recommendations)
    else:
        print(f"Unknown format type: {format_type}")

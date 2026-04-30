from typing import Any, Dict
from src.milestone_1.phase_2_preferences.schema import UserPreferences, BudgetPreference

def parse_preferences(data: Dict[str, Any]) -> UserPreferences:
    """
    Parses raw dictionary data into a UserPreferences object.
    Handles flat budget fields (min_cost, max_cost, category) if present.
    """
    if "budget" not in data:
        # Try to construct budget from flat fields
        mode = data.get("budget_mode", "category")
        if mode == "category":
            budget = BudgetPreference(mode="category", category=data.get("category", "medium"))
        else:
            budget = BudgetPreference(
                mode="range", 
                min_cost=data.get("min_cost"), 
                max_cost=data.get("max_cost")
            )
        data["budget"] = budget
    
    return UserPreferences(**data)

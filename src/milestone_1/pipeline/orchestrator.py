from src.milestone_1.phase_2_preferences.schema import UserPreferences, Recommendation
from src.milestone_1.phase_6_api.service import run_recommendation_pipeline

class Orchestrator:
    """
    Orchestrates the end-to-end recommendation process by calling the service layer.
    """
    @staticmethod
    def run(prefs: UserPreferences) -> list[Recommendation]:
        """
        Runs the full pipeline for given preferences.
        """
        return run_recommendation_pipeline(prefs)

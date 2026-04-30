from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.milestone_1.phase_2_preferences.schema import UserPreferences
from src.milestone_1.phase_6_api.service import run_recommendation_pipeline
from src.milestone_1.phase_0_setup.utils import logger

router = APIRouter()

@router.post("/recommend", response_model=Dict[str, Any])
async def get_recommendations(prefs: UserPreferences):
    """
    API endpoint to get restaurant recommendations based on user preferences.
    """
    logger.info(f"API Request received for location: {prefs.location}")
    try:
        recommendations = run_recommendation_pipeline(prefs)
        
        if not recommendations:
            return {
                "ok": True,
                "recommendations": [],
                "message": "No restaurants found matching your criteria."
            }
            
        return {
            "ok": True,
            "recommendations": [rec.model_dump() for rec in recommendations]
        }
    except Exception as e:
        logger.error(f"API processing error: {e}")
        return {"ok": False, "error": str(e)}

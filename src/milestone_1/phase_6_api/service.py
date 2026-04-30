from src.milestone_1.phase_1_ingestion.loader import fetch_data
from src.milestone_1.phase_1_ingestion.preprocess import clean_and_transform
from src.milestone_1.phase_2_preferences.schema import UserPreferences, Recommendation
from src.milestone_1.phase_3_candidates.filter import apply_filters
from src.milestone_1.phase_3_candidates.ranker import rank_candidates
from src.milestone_1.phase_4_llm.recommender import get_llm_recommendations
from src.milestone_1.phase_0_setup.utils import logger

# Cache the dataset in memory to avoid repeated loads
_cached_restaurants = []

def get_all_restaurants():
    """
    Returns all restaurants from the dataset, loading and preprocessing if not already cached.
    """
    global _cached_restaurants
    if not _cached_restaurants:
        df = fetch_data()
        if not df.empty:
            _cached_restaurants = clean_and_transform(df)
            logger.info(f"Loaded and cached {len(_cached_restaurants)} restaurants.")
        else:
            logger.error("Dataset is empty or could not be loaded.")
    return _cached_restaurants

def run_recommendation_pipeline(prefs: UserPreferences) -> list[Recommendation]:
    """
    Executes the full recommendation pipeline (filtering -> candidate selection -> LLM ranking).
    """
    logger.info(f"Running recommendation pipeline for location: {prefs.location}")
    
    all_restaurants = get_all_restaurants()
    if not all_restaurants:
        logger.error("No restaurants available to process.")
        return []
        
    # Phase 3: Candidate Selection (Filter & Basic Rank)
    filtered = apply_filters(all_restaurants, prefs)
    candidate_set = rank_candidates(filtered, prefs, top_k=20)
    
    # Phase 4: LLM Ranking & Explanation
    recommendations = get_llm_recommendations(candidate_set, top_k=5)
    
    return recommendations

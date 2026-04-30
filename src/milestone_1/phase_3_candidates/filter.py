from typing import List, Any
from src.milestone_1.phase_2_preferences.schema import RestaurantRecord, UserPreferences
from src.milestone_1.phase_0_setup.config import AppConfig, get_config
from src.milestone_1.phase_0_setup.utils import logger

def _normalize(s: Any) -> str:
    """Aggressively normalize strings for matching."""
    if s is None:
        return ""
    return "".join(str(s).lower().split())

def _budget_allows(r: RestaurantRecord, prefs: UserPreferences) -> bool:
    if prefs.budget.mode == "category":
        if r.price_category in (None, "", "unknown"):
            return True
        return r.price_category == prefs.budget.category
    
    if r.cost is None:
        return True
    if prefs.budget.min_cost is not None and r.cost < prefs.budget.min_cost:
        return False
    if prefs.budget.max_cost is not None and r.cost > prefs.budget.max_cost:
        return False
    return True

def _location_allows(r: RestaurantRecord, prefs: UserPreferences) -> bool:
    want = _normalize(prefs.location)
    have = _normalize(r.location)
    
    if not want: 
        return True
    if not have: 
        return False
        
    # Partial match: "btm" in "btmlayout", "koramangala" in "koramangala5thblock"
    return want in have or have in want

def _rating_allows(r: RestaurantRecord, prefs: UserPreferences, cfg: AppConfig) -> bool:
    min_rating = prefs.min_rating if prefs.min_rating is not None else cfg.default_min_rating
    max_rating = prefs.max_rating if prefs.max_rating is not None else 5.0
    if r.rating is None: return True
    return min_rating <= r.rating <= max_rating

def _cuisine_allows(r: RestaurantRecord, prefs: UserPreferences) -> bool:
    want_list = [c.strip().lower() for c in prefs.cuisines if c.strip()]
    if not want_list: 
        return True
        
    have = set([c.lower() for c in r.cuisines])
    if not have: 
        return False
        
    # Any-match (partial match for cuisines too?)
    for w in want_list:
        w_norm = _normalize(w)
        for h in have:
            if w_norm in _normalize(h):
                return True
    return False

def apply_filters(restaurants: List[RestaurantRecord], prefs: UserPreferences) -> List[RestaurantRecord]:
    """
    Applies detailed filters (location, rating, cuisines, budget) with debug logging.
    Order: Location -> Cuisine -> Budget -> Rating
    """
    cfg = get_config()
    total_start = len(restaurants)
    
    # 1. Location
    loc_filtered = [r for r in restaurants if _location_allows(r, prefs)]
    logger.info(f"Location filter: {len(loc_filtered)}/{total_start} matches for '{prefs.location}'")
    
    # Fallback: If no location matches, use all restaurants (Bangalore-wide)
    is_fallback = False
    if not loc_filtered and prefs.location:
        logger.warning(f"No matches for location '{prefs.location}'. Falling back to all of Bangalore.")
        loc_filtered = restaurants
        is_fallback = True
        
    # 2. Cuisine
    cuisine_filtered = [r for r in loc_filtered if _cuisine_allows(r, prefs)]
    logger.info(f"Cuisine filter: {len(cuisine_filtered)}/{len(loc_filtered)} matches")
    
    # 3. Budget
    budget_filtered = [r for r in cuisine_filtered if _budget_allows(r, prefs)]
    logger.info(f"Budget filter: {len(budget_filtered)}/{len(cuisine_filtered)} matches")
    
    # 4. Rating
    rating_filtered = [r for r in budget_filtered if _rating_allows(r, prefs, cfg)]
    logger.info(f"Rating filter: {len(rating_filtered)}/{len(budget_filtered)} matches")
    
    return rating_filtered

from typing import List
from src.milestone_1.phase_2_preferences.schema import RestaurantRecord, CandidateRestaurant, CandidateSet, UserPreferences

def _score(r: RestaurantRecord, prefs: UserPreferences) -> float:
    """
    Lightweight deterministic scoring for candidate ranking.
    """
    score = 0.0

    # Rating weight
    if r.rating is not None:
        score += float(r.rating) * 2.0

    # Cuisine match boost
    have = set([c.lower() for c in r.cuisines])
    want = set([c.strip().lower() for c in prefs.cuisines if c.strip()])
    score += float(len(have.intersection(want))) * 1.5

    # Budget fit boost
    if prefs.budget.mode == "category":
        if r.price_category == prefs.budget.category:
            score += 1.0
    else:
        if r.cost is not None and prefs.budget.min_cost is not None and prefs.budget.max_cost is not None:
            mid = (prefs.budget.min_cost + prefs.budget.max_cost) / 2.0
            score += max(0.0, 1.0 - (abs(float(r.cost) - mid) / max(1.0, mid))) * 1.0

    return score

def rank_candidates(filtered_restaurants: List[RestaurantRecord], prefs: UserPreferences, top_k: int = 20) -> CandidateSet:
    """
    Ranks candidates using deterministic scoring and returns a CandidateSet.
    """
    # Create scored list
    scored = [(r, _score(r, prefs)) for r in filtered_restaurants]
    
    # Sort key: score desc, then rating desc, then name asc
    def sort_key(item):
        r, score = item
        rating = r.rating if r.rating is not None else -1.0
        name = r.name.strip().lower()
        return (-score, -rating, name)
        
    scored.sort(key=sort_key)
    top = scored[:top_k]
    
    candidates = [
        CandidateRestaurant(
            id=r.id,
            name=r.name,
            location=r.location,
            cuisines=r.cuisines,
            rating=r.rating,
            cost=r.cost,
            price_category=r.price_category
        )
        for r, score in top
    ]
    
    return CandidateSet(user_preferences=prefs, candidates=candidates)

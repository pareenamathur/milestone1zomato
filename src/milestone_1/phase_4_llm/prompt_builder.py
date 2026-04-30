from src.milestone_1.phase_2_preferences.schema import CandidateSet

def build_prompt_payload(candidate_set: CandidateSet) -> dict:
    """
    Build the payload for the LLM prompt including user preferences and candidate list.
    Ensures clear instructions for distinct recommendations.
    """
    candidates_json = [c.model_dump() for c in candidate_set.candidates]
    prefs_dict = candidate_set.user_preferences.model_dump()
    
    system_instruction = (
        "You are a helpful restaurant recommendation assistant. "
        "Your task is to recommend the top 5 BEST restaurants based on the user's preferences. "
        "IMPORTANT RULES:\n"
        "1. You MUST ONLY select restaurants from the provided 'candidate_restaurants' list.\n"
        "2. Do NOT repeat restaurants. Every recommendation must be for a DISTINCT restaurant.\n"
        "3. Provide a helpful, personalized explanation for WHY you chose each restaurant.\n"
        "4. If multiple candidates are similar, prioritize those with higher ratings and better alignment with cuisines.\n"
        "5. Return EXACTLY top 5 recommendations unless fewer than 5 candidates are provided."
    )
    
    payload = {
        "system_instruction": system_instruction,
        "user_preferences": prefs_dict,
        "candidate_restaurants": candidates_json
    }
    
    return payload

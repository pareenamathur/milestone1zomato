import os
import json
import time
from groq import Groq
from typing import List, Optional
from src.milestone_1.phase_2_preferences.schema import CandidateSet, Recommendation
from src.milestone_1.phase_4_llm.prompt_builder import build_prompt_payload
from src.milestone_1.phase_0_setup.utils import log_llm_latency, log_llm_failure, log_fallback_usage, log_no_results, logger

class GroqClient:
    """
    Client for interacting with the Groq API.
    """
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
    def get_recommendations(self, prompt_payload: dict, top_k: int) -> str | None:
        if not self.client:
            return None
            
        system_msg = prompt_payload.get("system_instruction", "You are a helpful assistant.")
        
        user_msg = json.dumps({
            "user_preferences": prompt_payload.get("user_preferences"),
            "candidate_restaurants": prompt_payload.get("candidate_restaurants")
        })
        
        user_msg += f"\n\nPlease select the top {top_k} DISTINCT restaurants from the candidates and return a JSON object containing a single key 'recommendations' mapped to a list of objects. Each object must have: 'rank' (int), 'restaurant_id' (str), 'restaurant_name' (str), and 'explanation' (str)."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            log_llm_failure(f"Groq API Error: {e}")
            return None

def parse_and_validate(json_str: str, candidate_set: CandidateSet) -> list[Recommendation]:
    """
    Parses LLM response and validates against candidates.
    Ensures uniqueness of recommended restaurants.
    """
    try:
        data = json.loads(json_str)
        recs_list = []
        if isinstance(data, dict):
            if "recommendations" in data and isinstance(data["recommendations"], list):
                recs_list = data["recommendations"]
            else:
                for v in data.values():
                    if isinstance(v, list):
                        recs_list = v
                        break
        elif isinstance(data, list):
            recs_list = data
            
        candidates_by_id = {c.id: c for c in candidate_set.candidates}
        recommendations = []
        seen_ids = set()
        seen_names = set()
        
        for item in recs_list:
            r_id = item.get("restaurant_id")
            name_from_llm = item.get("restaurant_name", "").strip().lower()
            
            if not r_id or r_id not in candidates_by_id or r_id in seen_ids:
                continue
                
            c = candidates_by_id[r_id]
            clean_name = c.name.strip().lower()
            
            # Extra safety: deduplicate by name as well
            if clean_name in seen_names:
                continue
                
            seen_ids.add(r_id)
            seen_names.add(clean_name)
            
            rec = Recommendation(
                rank=int(item.get("rank", len(recommendations) + 1)),
                restaurant_id=r_id,
                restaurant_name=c.name,
                cuisines=c.cuisines,
                rating=c.rating,
                estimated_cost=c.cost,
                explanation=str(item.get("explanation", "Recommended based on your preferences."))
            )
            recommendations.append(rec)
            
        recommendations.sort(key=lambda x: x.rank)
        return recommendations[:5]
    except Exception as e:
        log_llm_failure(f"JSON Parsing Error: {e}")
        return []

def fallback_ranking(candidate_set: CandidateSet, top_k: int) -> list[Recommendation]:
    """
    Mechanical fallback that takes the pre-ranked top_k.
    Ensures uniqueness.
    """
    log_fallback_usage()
    recommendations = []
    seen_ids = set()
    seen_names = set()
    
    # Sort candidates by rating and cost fit if possible
    sorted_candidates = sorted(
        candidate_set.candidates, 
        key=lambda x: (x.rating or 0, -(x.cost or 10000)), 
        reverse=True
    )
    
    for c in sorted_candidates:
        clean_name = c.name.strip().lower()
        if c.id in seen_ids or clean_name in seen_names: 
            continue
            
        seen_ids.add(c.id)
        seen_names.add(clean_name)
        
        rec = Recommendation(
            rank=len(recommendations) + 1,
            restaurant_id=c.id,
            restaurant_name=c.name,
            cuisines=c.cuisines,
            rating=c.rating,
            estimated_cost=c.cost,
            explanation="Highly rated restaurant matching your criteria."
        )
        recommendations.append(rec)
        if len(recommendations) >= top_k:
            break
            
    return recommendations

def get_llm_recommendations(candidate_set: CandidateSet, top_k: int = 5) -> List[Recommendation]:
    """
    Main entry point for Phase 4 LLM recommendations.
    """
    if not candidate_set.candidates:
        log_no_results()
        return []
        
    payload = build_prompt_payload(candidate_set)
    client = GroqClient()
    
    if not client.client:
        log_llm_failure("GroqClient not initialized (missing API key)")
        return fallback_ranking(candidate_set, top_k)
        
    start_time = time.time()
    response_json = client.get_recommendations(payload, top_k)
    duration_ms = (time.time() - start_time) * 1000
    
    if not response_json:
        return fallback_ranking(candidate_set, top_k)
        
    log_llm_latency(duration_ms)
    valid_recs = parse_and_validate(response_json, candidate_set)
    
    if not valid_recs:
        return fallback_ranking(candidate_set, top_k)
        
    return valid_recs

import logging
import json
from typing import Any

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        if hasattr(record, "metrics"):
            log_obj["metrics"] = record.metrics
        return json.dumps(log_obj)

# Setup root logger
logger = logging.getLogger("recommender")
logger.setLevel(logging.INFO)

# Only add handler if not already present
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(JSONFormatter())
    logger.addHandler(ch)

def log_input_summary(preferences: Any):
    logger.info(
        "User preferences received",
        extra={"metrics": {"event_type": "input_summary", "location": preferences.location, "cuisines": preferences.cuisines}}
    )

def log_filter_metrics(initial_count: int, final_count: int):
    logger.info(
        "Candidate filtering completed",
        extra={"metrics": {"event_type": "filter_counts", "initial_count": initial_count, "final_count": final_count}}
    )

def log_llm_latency(duration_ms: float):
    logger.info(
        "LLM recommendation generated",
        extra={"metrics": {"event_type": "llm_latency", "duration_ms": duration_ms}}
    )

def log_llm_failure(reason: str):
    logger.error(
        f"LLM request failed: {reason}",
        extra={"metrics": {"event_type": "llm_failure", "reason": reason}}
    )

def log_fallback_usage():
    logger.warning(
        "Using heuristic fallback ranking",
        extra={"metrics": {"event_type": "fallback_usage"}}
    )

def log_no_results():
    logger.info(
        "No results found matching criteria",
        extra={"metrics": {"event_type": "no_results"}}
    )

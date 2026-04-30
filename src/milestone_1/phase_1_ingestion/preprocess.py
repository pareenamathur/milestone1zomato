import pandas as pd
import hashlib
import re
from typing import List, Any
from src.milestone_1.phase_2_preferences.schema import RestaurantRecord
from src.milestone_1.phase_0_setup.config import AppConfig, get_config
from src.milestone_1.phase_0_setup.utils import logger

_NUMBER_RE = re.compile(r"(\d+(?:[,\s]\d+)*)")

def _pick_column(columns: list[str], preferred: str, fallbacks: list[str]) -> str | None:
    if preferred in columns:
        return preferred
    lowered = {c.lower(): c for c in columns}
    if preferred.lower() in lowered:
        return lowered[preferred.lower()]
    for fb in fallbacks:
        if fb in columns:
            return fb
        if fb.lower() in lowered:
            return lowered[fb.lower()]
    return None

def _stable_id(name: str, location: str) -> str:
    """Generate a stable ID based on name and location only."""
    base = f"{name.lower()}|{location.lower()}".encode("utf-8", errors="ignore")
    return hashlib.md5(base).hexdigest()[:16]

def parse_rating(value: Any) -> float | None:
    if value is None: return None
    if isinstance(value, (int, float)):
        r = float(value)
    else:
        s = " ".join(str(value).strip().split())
        if not s or s.upper() in {"NEW", "N/A", "--", "NA"}: return None
        s = s.replace(",", ".")
        if "/" in s: s = s.split("/", 1)[0].strip()
        try: r = float(s)
        except ValueError: return None
    return r if 0 <= r <= 5 else None

def parse_cost(value: Any) -> int | None:
    if value is None or isinstance(value, bool): return None
    if isinstance(value, (int, float)):
        c = int(value)
        return c if c >= 0 else None
    s = " ".join(str(value).strip().split())
    if not s or s.upper() in {"N/A", "--", "NA"}: return None
    m = _NUMBER_RE.search(s)
    if not m: return None
    digits = re.sub(r"[,\s]", "", m.group(1))
    try:
        c = int(digits)
        return c if c >= 0 else None
    except ValueError: return None

def clean_and_transform(df: pd.DataFrame, cfg: AppConfig | None = None) -> List[RestaurantRecord]:
    cfg = cfg or get_config()
    cols = list(df.columns)

    col_name = _pick_column(cols, cfg.col_name, ["name", "restaurant name", "Restaurant"])
    col_location = _pick_column(cols, cfg.col_location, ["location", "city", "Locality"])
    col_cuisines = _pick_column(cols, cfg.col_cuisines, ["cuisine", "cuisines"])
    col_rating = _pick_column(cols, cfg.col_rating, ["rating", "rate", "Aggregate rating"])
    col_cost = _pick_column(cols, cfg.col_cost, ["cost", "approx_cost(for two people)", "Average Cost for two"])

    records: List[RestaurantRecord] = []
    seen = set()
    duplicate_count = 0
    
    for idx, row in df.iterrows():
        try:
            name = " ".join(str(row.get(col_name)).strip().split())
            location = " ".join(str(row.get(col_location)).strip().split()).lower()
            if not name or not location: continue

            # Deduplication
            restaurant_key = (name.lower(), location.lower())
            if restaurant_key in seen:
                duplicate_count += 1
                continue
            seen.add(restaurant_key)

            cuisines = [c.strip().lower() for c in str(row.get(col_cuisines)).replace("|", ",").split(",")] if col_cuisines else []
            rating = parse_rating(row.get(col_rating)) if col_rating else None
            cost = parse_cost(row.get(col_cost)) if col_cost else None
            
            # Price category
            price_category = "unknown"
            if cost is not None:
                if cost <= cfg.budget_low_max: price_category = "low"
                elif cost <= cfg.budget_medium_max: price_category = "medium"
                else: price_category = "high"

            rec = RestaurantRecord(
                id=_stable_id(name, location),
                name=name,
                location=location,
                cuisines=[c for c in cuisines if c],
                rating=rating,
                cost=cost,
                price_category=price_category,
                raw={}
            )
            records.append(rec)
        except Exception: continue
        
    logger.info(f"Preprocessing complete. Total unique: {len(records)}, Duplicates skipped: {duplicate_count}")
    return records

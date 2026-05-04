from datasets import load_dataset
from src.milestone_1.phase_0_setup.config import AppConfig, get_config
from src.milestone_1.phase_0_setup.utils import logger

def fetch_data(cfg: AppConfig | None = None) -> list[dict]:
    """
    Loads raw dataset into a list of dictionaries.
    ULTRA-OPTIMIZED for memory:
    1. Uses streaming=True to avoid downloading full dataset.
    2. Strictly limits to 500 rows.
    3. Avoids Pandas overhead entirely.
    """
    cfg = cfg or get_config()
    logger.info(f"Fetching data from Hugging Face (STREAMING): {cfg.dataset_id}")
    
    usecols = [cfg.col_name, cfg.col_location, cfg.col_cuisines, cfg.col_rating, cfg.col_cost]
    
    try:
        # streaming=True ensures we don't load the entire 50k+ rows into memory.
        # It yields one row at a time.
        ds = load_dataset(cfg.dataset_id, split='train', streaming=True)
        
        records = []
        count = 0
        for row in ds:
            # Only pick the columns we need
            record = {col: row.get(col) for col in usecols if col in row}
            
            # Basic validation: ensure we have at least name and location
            if record.get(cfg.col_name) and record.get(cfg.col_location):
                records.append(record)
                count += 1
            
            if count >= 500:
                break
                
        logger.info(f"Successfully fetched {len(records)} records using streaming.")
        return records
    except Exception as e:
        logger.error(f"Failed to fetch data using streaming: {e}")
        return []

import pandas as pd
from pathlib import Path
from datasets import load_dataset
from src.milestone_1.phase_0_setup.config import AppConfig, get_config
from src.milestone_1.phase_0_setup.utils import logger

def fetch_data(cfg: AppConfig | None = None) -> pd.DataFrame:
    """
    Loads raw dataset into a pandas DataFrame.
    Optimized for memory: loads only required columns and limits to 2000 rows.
    """
    cfg = cfg or get_config()
    logger.info(f"Checking for local dataset in {cfg.cache_dir}...")
    
    usecols = ['name', 'location', 'cuisines', 'rate', 'approx_cost(for two people)']
    
    local_csv = Path(cfg.cache_dir) / "zomato.csv"
    if local_csv.exists():
        logger.info(f"Loading raw dataset from local file: {local_csv}")
        try:
            # We drop NaNs in core columns early and strictly limit to 500 rows during read
            df = pd.read_csv(local_csv, usecols=lambda c: c in usecols, nrows=500)
            df = df.dropna(subset=[c for c in ['location', 'cuisines', 'rate', 'approx_cost(for two people)'] if c in df.columns])
            return df
        except Exception as e:
            logger.error(f"Failed to read local CSV: {e}")
    
    logger.info(f"Local file not found or failed. Fetching from Hugging Face: {cfg.dataset_id}")
    try:
        # EXTREME MEMORY OPTIMIZATION: Max 500 rows to ensure we stay well below 512MB
        ds = load_dataset(cfg.dataset_id, split='train[:500]')
        
        # Select ONLY required columns BEFORE converting to Pandas.
        # This prevents loading heavy text arrays (like reviews) into RAM.
        existing_cols = [c for c in usecols if c in ds.column_names]
        ds = ds.select_columns(existing_cols)
        
        df = ds.to_pandas()
        
        # Drop rows with missing critical info
        critical_cols = [c for c in ['location', 'cuisines', 'rate', 'approx_cost(for two people)'] if c in df.columns]
        if critical_cols:
            df = df.dropna(subset=critical_cols)
            
        return df
    except Exception as e:
        logger.error(f"Failed to fetch data from Hugging Face: {e}")
        return pd.DataFrame()

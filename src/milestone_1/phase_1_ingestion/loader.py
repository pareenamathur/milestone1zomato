import pandas as pd
from pathlib import Path
from datasets import load_dataset
from src.milestone_1.phase_0_setup.config import AppConfig, get_config
from src.milestone_1.phase_0_setup.utils import logger

def fetch_data(cfg: AppConfig | None = None) -> pd.DataFrame:
    """
    Loads raw dataset into a pandas DataFrame.
    Prefers locally downloaded CSV if present in cache.
    """
    cfg = cfg or get_config()
    logger.info(f"Checking for local dataset in {cfg.cache_dir}...")
    
    local_csv = Path(cfg.cache_dir) / "zomato.csv"
    if local_csv.exists():
        logger.info(f"Loading raw dataset from local file: {local_csv}")
        try:
            # We drop NaNs in core columns early to keep the DF manageable
            return pd.read_csv(local_csv).dropna(subset=['location', 'cuisines', 'rate', 'approx_cost(for two people)'])
        except Exception as e:
            logger.error(f"Failed to read local CSV: {e}")
    
    logger.info(f"Local file not found or failed. Fetching from Hugging Face: {cfg.dataset_id}")
    try:
        ds_dict = load_dataset(cfg.dataset_id)
        split_name = "train" if "train" in ds_dict else next(iter(ds_dict.keys()))
        ds = ds_dict[split_name]
        return ds.to_pandas()
    except Exception as e:
        logger.error(f"Failed to fetch data from Hugging Face: {e}")
        return pd.DataFrame()

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """
    Central configuration for the recommender.
    """

    model_config = SettingsConfigDict(
        env_prefix="M1_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Data source
    dataset_id: str = Field(
        default="ManikaSaini/zomato-restaurant-recommendation",
        description="Hugging Face dataset identifier.",
    )

    # Column mapping (dataset → canonical fields).
    col_name: str = Field(default="name", description="Column for restaurant name.")
    col_location: str = Field(default="location", description="Column for restaurant location/city.")
    col_cuisines: str = Field(default="cuisines", description="Column for cuisines.")
    col_rating: str = Field(default="rate", description="Column for rating.")
    col_cost: str = Field(default="approx_cost(for two people)", description="Column for cost.")

    # Local caching / persistence
    cache_dir: Path = Field(default=Path(".cache"), description="Cache directory.")
    cleaned_data_path: Path = Field(
        default=Path(".cache/cleaned_restaurants.parquet"),
        description="Path for persisted cleaned dataset.",
    )

    # Candidate selection + output sizing
    top_k_candidates: int = Field(
        default=50,
        ge=5,
        le=200,
        description="Max candidates to pass into the LLM prompt.",
    )
    top_k_recommendations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of recommendations to display to the user.",
    )

    # Defaults / thresholds
    default_min_rating: float = Field(
        default=3.5,
        ge=0,
        le=5,
        description="Default minimum rating if the user does not specify one.",
    )

    # Budget strategy
    budget_mode: Literal["category", "range"] = Field(
        default="category",
        description="How budget is interpreted: category (low/medium/high) or numeric range.",
    )
    budget_low_max: int = Field(default=300, ge=0, description="Max cost for low budget.")
    budget_medium_max: int = Field(default=700, ge=0, description="Max cost for medium budget.")

    # LLM settings
    llm_provider: str = Field(default="openai", description="LLM provider name.")
    llm_model: str = Field(default="gpt-4.1-mini", description="LLM model name.")
    llm_temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    llm_timeout_s: int = Field(default=30, ge=5, le=300)

    def ensure_paths(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_data_path.parent.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    cfg = AppConfig()
    cfg.ensure_paths()
    return cfg

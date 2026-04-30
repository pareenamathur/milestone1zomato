from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class BudgetPreference(BaseModel):
    """
    Budget can be expressed either as a category or an explicit numeric range.
    Only one representation is required.
    """

    mode: Literal["category", "range"] = "category"
    category: Literal["low", "medium", "high"] | None = None
    min_cost: int | None = Field(default=None, ge=0)
    max_cost: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _validate_budget(self) -> "BudgetPreference":
        if self.mode == "category":
            if self.category is None:
                raise ValueError("budget.category is required when budget.mode='category'")
        else:
            if self.min_cost is None and self.max_cost is None:
                raise ValueError(
                    "At least one of budget.min_cost or budget.max_cost is required when budget.mode='range'"
                )
            if (
                self.min_cost is not None
                and self.max_cost is not None
                and self.min_cost > self.max_cost
            ):
                raise ValueError("budget.min_cost must be <= budget.max_cost")
        return self


class UserPreferences(BaseModel):
    location: str = Field(min_length=1, description="City/location preference.")
    budget: BudgetPreference
    cuisines: list[str] = Field(min_length=1, description="Preferred cuisines (1+).")
    min_rating: float | None = Field(default=None, ge=0, le=5)
    max_rating: float | None = Field(default=5.0, ge=0, le=5)
    extra_preferences: list[str] = Field(default_factory=list)

    @field_validator("location")
    @classmethod
    def _normalize_location(cls, v: str) -> str:
        return " ".join(v.strip().split())

    @field_validator("cuisines", mode="before")
    @classmethod
    def _normalize_cuisines(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            parts = [p.strip() for p in v.replace("|", ",").split(",")]
            v = [p for p in parts if p]
        if not isinstance(v, list) or not v:
            raise ValueError("cuisines must be a non-empty list or comma-separated string")
        normalized: list[str] = []
        seen = set()
        for item in v:
            s = " ".join(str(item).strip().split()).lower()
            if s and s not in seen:
                normalized.append(s)
                seen.add(s)
        if not normalized:
            raise ValueError("cuisines must include at least one non-empty value")
        return normalized

    @field_validator("extra_preferences", mode="before")
    @classmethod
    def _normalize_extra_preferences(cls, v: Any) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            parts = [p.strip() for p in v.replace("|", ",").split(",")]
            v = [p for p in parts if p]
        if not isinstance(v, list):
            raise ValueError("extra_preferences must be a list or comma-separated string")
        out: list[str] = []
        seen = set()
        for item in v:
            s = " ".join(str(item).strip().split()).lower()
            if s and s not in seen:
                out.append(s)
                seen.add(s)
        return out


class RestaurantRecord(BaseModel):
    """
    Canonical normalized restaurant record produced by preprocessing.
    """

    id: str = Field(min_length=1, description="Stable identifier for the record.")
    name: str = Field(min_length=1)
    location: str = Field(min_length=1, description="Canonical city/location.")
    cuisines: list[str] = Field(default_factory=list, description="Canonical cuisine tags.")
    rating: float | None = Field(default=None, ge=0, le=5)
    cost: int | None = Field(default=None, ge=0, description="Estimated cost (dataset-specific).")
    price_category: Literal["low", "medium", "high", "unknown"] = "unknown"
    raw: dict[str, Any] = Field(default_factory=dict, description="Original raw row fields.")

    @field_validator("cuisines", mode="before")
    @classmethod
    def _normalize_record_cuisines(cls, v: Any) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            parts = [p.strip() for p in v.replace("|", ",").split(",")]
            v = [p for p in parts if p]
        if not isinstance(v, list):
            raise ValueError("cuisines must be a list or string")
        out: list[str] = []
        seen = set()
        for item in v:
            s = " ".join(str(item).strip().split()).lower()
            if s and s not in seen:
                out.append(s)
                seen.add(s)
        return out

    @field_validator("location")
    @classmethod
    def _normalize_record_location(cls, v: str) -> str:
        return " ".join(v.strip().split()).lower()


class CandidateRestaurant(BaseModel):
    """
    Compact representation of a restaurant for prompting and display.
    """

    id: str
    name: str
    location: str
    cuisines: list[str] = Field(default_factory=list)
    rating: float | None = None
    cost: int | None = None
    price_category: str | None = None


class CandidateSet(BaseModel):
    user_preferences: UserPreferences
    candidates: list[CandidateRestaurant] = Field(min_length=1)


class Recommendation(BaseModel):
    """
    Final recommendation object shown to users.
    """

    rank: int = Field(ge=1)
    restaurant_id: str
    restaurant_name: str
    cuisines: list[str] = Field(default_factory=list)
    rating: float | None = None
    estimated_cost: int | None = None
    explanation: str = Field(min_length=1, description="1–3 sentence, preference-aware explanation.")

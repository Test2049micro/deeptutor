"""Request config for meta-analysis capability."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class OutlineItem(BaseModel):
    title: str = ""
    overview: str = ""


class MetaAnalysisRequestConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = ""
    depth: Literal["quick", "standard", "deep", "manual"] = "standard"
    max_studies: int = 20
    min_quality: Literal["low", "medium", "high"] = "medium"
    effect_type: Literal["auto", "mean_difference", "standardized_mean_difference", "odds_ratio", "risk_ratio"] = "auto"
    include_retracted: bool = False
    language: Literal["all", "en", "zh"] = "all"
    confirmed_outline: list[OutlineItem] | None = None

    @field_validator("max_studies")
    @classmethod
    def validate_max_studies(cls, value: int) -> int:
        return max(1, min(value, 100))


def validate_meta_analysis_request_config(raw_config: dict[str, Any] | None) -> MetaAnalysisRequestConfig:
    if not isinstance(raw_config, dict):
        raise ValueError("Meta-analysis requires an explicit config object.")
    try:
        return MetaAnalysisRequestConfig.model_validate(raw_config)
    except ValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise ValueError(f"Invalid meta-analysis config: {details}") from exc


__all__ = [
    "MetaAnalysisRequestConfig",
    "validate_meta_analysis_request_config",
]

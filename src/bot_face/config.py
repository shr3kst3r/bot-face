"""Configuration models and options for avatar generation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class AvatarConfig(BaseModel):
    """Configuration options for generating a cute robot avatar."""

    seed: Any = Field(
        default=None,
        description="Seed value (string, integer, bytes, or None for random).",
    )
    size: int = Field(
        default=256,
        ge=16,
        le=4096,
        description="Width and height of the rendered avatar in pixels.",
    )
    corner_radius: int = Field(
        default=0,
        ge=0,
        description="Corner radius in pixels for rounded rectangle clipping (0 = sharp square).",
    )
    circle: bool = Field(
        default=False,
        description="Clip the avatar to a complete circle (overrides corner_radius).",
    )
    palette: str | None = Field(
        default=None,
        description="Name of color palette to use. If None, chosen from seed.",
    )
    filter: str | None = Field(
        default=None,
        description="Optional retro style or filter: '8bit', '16bit', 'gameboy', 'crt', etc.",
    )
    has_hat: bool | None = Field(
        default=None,
        description="Force hat presence (True/False). If None, sampled from seed.",
    )
    has_glasses: bool | None = Field(
        default=None,
        description="Force glasses/eyewear presence (True/False). If None, sampled from seed.",
    )
    has_badge: bool | None = Field(
        default=None,
        description="Force chest badge presence (True/False). If None, sampled from seed.",
    )
    cat: bool | None = Field(
        default=None,
        description="Force cute cat robot features (cat ears, whiskers, cat mouth, bell collar).",
    )

    @field_validator("corner_radius")
    @classmethod
    def validate_corner_radius(cls, v: int) -> int:
        if v < 0:
            msg = "corner_radius must be non-negative"
            raise ValueError(msg)
        return v

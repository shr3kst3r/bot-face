"""bot-face: Cute robot avatar generator library and CLI for account profile images."""

from __future__ import annotations

from typing import Any

from bot_face.colors import PALETTES, ColorPalette, get_palette, list_palettes
from bot_face.config import AvatarConfig
from bot_face.generator import generate
from bot_face.models import RobotAvatar

__version__ = "0.1.0"


def render_svg(
    seed: Any = None,
    size: int = 256,
    corner_radius: int = 0,
    circle: bool = False,
    palette: str | None = None,
    has_hat: bool | None = None,
    has_glasses: bool | None = None,
    has_badge: bool | None = None,
) -> str:
    """Convenience helper to generate an avatar and return its standalone SVG string."""
    avatar = generate(
        seed=seed,
        size=size,
        corner_radius=corner_radius,
        circle=circle,
        palette=palette,
        has_hat=has_hat,
        has_glasses=has_glasses,
        has_badge=has_badge,
    )
    return avatar.to_svg()


def render_png(
    seed: Any = None,
    size: int = 256,
    corner_radius: int = 0,
    circle: bool = False,
    palette: str | None = None,
    has_hat: bool | None = None,
    has_glasses: bool | None = None,
    has_badge: bool | None = None,
) -> bytes:
    """Convenience helper to generate an avatar and return encoded PNG bytes."""
    avatar = generate(
        seed=seed,
        size=size,
        corner_radius=corner_radius,
        circle=circle,
        palette=palette,
        has_hat=has_hat,
        has_glasses=has_glasses,
        has_badge=has_badge,
    )
    return avatar.to_bytes("png")


__all__ = [
    "PALETTES",
    "AvatarConfig",
    "ColorPalette",
    "RobotAvatar",
    "__version__",
    "generate",
    "get_palette",
    "list_palettes",
    "render_png",
    "render_svg",
]

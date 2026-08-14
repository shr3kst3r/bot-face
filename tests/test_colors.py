"""Tests for color palettes and conversion utilities."""

from __future__ import annotations

import pytest

from bot_face.colors import (
    PALETTES,
    get_palette,
    hex_to_rgb,
    hex_to_rgba,
    list_palettes,
)


def test_list_palettes() -> None:
    palettes = list_palettes()
    assert len(palettes) >= 10
    assert "bubblegum" in palettes
    assert "cyber_mint" in palettes
    assert "sunny_lemon" in palettes
    assert sorted(palettes) == palettes


def test_get_palette_valid() -> None:
    p = get_palette("bubblegum")
    assert p.name == "bubblegum"
    assert p.chassis.startswith("#")
    assert p.background.startswith("#")

    # Case insensitivity and hyphen/underscore normalization
    p_upper = get_palette("CYBER-MINT")
    assert p_upper.name == "cyber_mint"


def test_get_palette_invalid() -> None:
    with pytest.raises(ValueError, match="Unknown palette 'nonexistent'"):
        get_palette("nonexistent")


def test_all_palettes_valid_hex() -> None:
    for name in list_palettes():
        pal = PALETTES[name]
        for field_name in [
            "background",
            "background_alt",
            "chassis",
            "chassis_dark",
            "faceplate",
            "accent",
            "eye_primary",
            "eye_glow",
            "mouth",
            "cheek",
            "detail",
        ]:
            val = getattr(pal, field_name)
            rgb = hex_to_rgb(val)
            assert len(rgb) == 3
            assert all(0 <= c <= 255 for c in rgb)


def test_hex_to_rgb() -> None:
    assert hex_to_rgb("#FF0000") == (255, 0, 0)
    assert hex_to_rgb("00FF00") == (0, 255, 0)
    assert hex_to_rgb("#0000FF") == (0, 0, 255)
    # 3-char shorthand
    assert hex_to_rgb("#FFF") == (255, 255, 255)
    assert hex_to_rgb("000") == (0, 0, 0)


def test_hex_to_rgba() -> None:
    assert hex_to_rgba("#FF0000", alpha=128) == (255, 0, 0, 128)


def test_hex_to_rgb_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid hex color"):
        hex_to_rgb("not-a-hex")
    with pytest.raises(ValueError, match="Invalid hex color"):
        hex_to_rgb("#12345")

"""Tests for 8-bit, 16-bit, gameboy, and other visual filters."""

from __future__ import annotations

import pytest
from PIL import Image

from bot_face.filters import (
    apply_8bit_filter,
    apply_16bit_filter,
    apply_blueprint_filter,
    apply_crt_filter,
    apply_dither_filter,
    apply_filter,
    apply_gameboy_filter,
    apply_monochrome_filter,
    apply_neon_glow_filter,
    apply_sepia_filter,
    list_filters,
)
from bot_face.generator import generate


def test_list_filters() -> None:
    filters = list_filters()
    assert "8bit" in filters
    assert "16bit" in filters
    assert "gameboy" in filters
    assert "crt" in filters
    assert "blueprint" in filters
    assert "monochrome" in filters
    assert "sepia" in filters
    assert "dither" in filters
    assert "neon_glow" in filters


def test_apply_all_filters() -> None:
    bot = generate(seed="filter_test_bot", size=128)
    raw_img = bot.to_image()

    for f_name in list_filters():
        filtered = apply_filter(raw_img, f_name)
        assert isinstance(filtered, Image.Image)
        assert filtered.size == (128, 128)


def test_individual_filter_functions() -> None:
    base = Image.new("RGBA", (64, 64), (100, 150, 200, 255))

    assert apply_8bit_filter(base).size == (64, 64)
    assert apply_16bit_filter(base).size == (64, 64)
    assert apply_gameboy_filter(base).size == (64, 64)
    assert apply_crt_filter(base).size == (64, 64)
    assert apply_blueprint_filter(base).size == (64, 64)
    assert apply_monochrome_filter(base).size == (64, 64)
    assert apply_sepia_filter(base).size == (64, 64)
    assert apply_dither_filter(base).size == (64, 64)
    assert apply_neon_glow_filter(base).size == (64, 64)


def test_apply_filter_none() -> None:
    base = Image.new("RGBA", (64, 64), (100, 150, 200, 255))
    assert apply_filter(base, None) is base
    assert apply_filter(base, "none") is base


def test_apply_filter_invalid() -> None:
    base = Image.new("RGBA", (64, 64), (100, 150, 200, 255))
    with pytest.raises(ValueError, match="Unknown filter 'invalid_filter'"):
        apply_filter(base, "invalid_filter")


def test_generate_with_filter() -> None:
    bot = generate(seed="user_8bit", size=128, filter="8bit")
    img = bot.to_image()
    assert img.size == (128, 128)

    # Saved file should have filter applied
    png_bytes = bot.to_bytes("png")
    assert png_bytes.startswith(b"\x89PNG")

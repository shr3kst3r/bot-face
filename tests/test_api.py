"""Tests for the high-level bot_face public API."""

from __future__ import annotations

import bot_face


def test_top_level_exports() -> None:
    assert hasattr(bot_face, "generate")
    assert hasattr(bot_face, "render_svg")
    assert hasattr(bot_face, "render_png")
    assert hasattr(bot_face, "list_palettes")
    assert hasattr(bot_face, "get_palette")
    assert hasattr(bot_face, "__version__")


def test_render_svg_helper() -> None:
    svg_str = bot_face.render_svg(seed="helper_test", size=128, corner_radius=16)
    assert svg_str.startswith("<svg")
    assert 'width="128"' in svg_str


def test_render_png_helper() -> None:
    png_bytes = bot_face.render_png(seed="helper_test", size=128, circle=True)
    assert png_bytes.startswith(b"\x89PNG")


def test_jupyter_repr_methods() -> None:
    avatar = bot_face.generate(seed="jupyter_test")
    svg_repr = avatar._repr_svg_()
    assert svg_repr.startswith("<svg")

    png_repr = avatar._repr_png_()
    assert png_repr.startswith(b"\x89PNG")

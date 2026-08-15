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


def test_html_and_react_helpers() -> None:
    avatar = bot_face.generate(seed="react_test", size=128)
    html = avatar.to_html_img(alt="Custom Bot", class_name="avatar-img")
    assert '<img src="data:image/svg+xml;base64,' in html
    assert 'alt="Custom Bot"' in html
    assert 'class="avatar-img"' in html

    react_comp = avatar.to_react_component("MyRobotIcon")
    assert "export const MyRobotIcon" in react_comp
    assert "<svg" in react_comp


def test_save_iconset(tmp_path: bot_face.models.Path) -> None:
    avatar = bot_face.generate(seed="iconset_test")
    out_dir = tmp_path / "icons"
    results = avatar.save_iconset(out_dir)

    assert "favicon.ico" in results
    assert "apple-touch-icon.png" in results
    assert "site.webmanifest" in results
    assert "html_snippet.html" in results
    assert (out_dir / "favicon.ico").exists()
    assert (out_dir / "apple-touch-icon.png").exists()
    assert (out_dir / "site.webmanifest").exists()

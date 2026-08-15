"""Tests for Pillow raster rendering and image export formats."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from bot_face.generator import generate


def test_render_pillow_image_dimensions() -> None:
    bot = generate(seed="raster_test", size=128)
    img = bot.to_image()

    assert isinstance(img, Image.Image)
    assert img.size == (128, 128)
    assert img.mode == "RGBA"


def test_raster_transparency_on_rounded_corners() -> None:
    bot = generate(seed="corner_test", size=128, corner_radius=32)
    img = bot.to_image()

    # The top-left corner (0, 0) should be transparent (alpha = 0)
    top_left_pixel = img.getpixel((0, 0))
    assert top_left_pixel[3] == 0

    # The center pixel (64, 64) should be fully opaque (alpha = 255)
    center_pixel = img.getpixel((64, 64))
    assert center_pixel[3] == 255


def test_raster_circle_clip() -> None:
    bot = generate(seed="circle_raster_test", size=128, circle=True)
    img = bot.to_image()

    # Top-left corner transparent
    assert img.getpixel((0, 0))[3] == 0
    # Center opaque
    assert img.getpixel((64, 64))[3] == 255


def test_to_bytes_formats() -> None:
    bot = generate(seed="format_test", size=64)

    png_bytes = bot.to_bytes("png")
    assert png_bytes.startswith(b"\x89PNG")

    svg_bytes = bot.to_bytes("svg")
    assert svg_bytes.startswith(b"<svg")

    webp_bytes = bot.to_bytes("webp")
    assert len(webp_bytes) > 0

    jpg_bytes = bot.to_bytes("jpg")
    assert len(jpg_bytes) > 0


def test_to_data_uri() -> None:
    bot = generate(seed="uri_test", size=64)

    svg_uri = bot.to_data_uri("svg")
    assert svg_uri.startswith("data:image/svg+xml;base64,")

    png_uri = bot.to_data_uri("png")
    assert png_uri.startswith("data:image/png;base64,")


def test_save_inferred_extensions(tmp_path: Path) -> None:
    bot = generate(seed="save_test", size=64)

    png_file = tmp_path / "avatar.png"
    bot.save(png_file)
    assert png_file.exists()
    assert png_file.read_bytes().startswith(b"\x89PNG")

    svg_file = tmp_path / "avatar.svg"
    bot.save(svg_file)
    assert svg_file.exists()
    assert svg_file.read_text(encoding="utf-8").startswith("<svg")

    webp_file = tmp_path / "avatar.webp"
    bot.save(webp_file)
    assert webp_file.exists()

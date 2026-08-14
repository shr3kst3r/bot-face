"""Tests for SVG vector rendering."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from bot_face.generator import (
    ALL_BADGE_STYLES,
    ALL_EYE_STYLES,
    ALL_HAT_STYLES,
    ANTENNA_STYLES,
    FACEPLATE_STYLES,
    HEAD_STYLES,
    MOUTH_STYLES,
    TORSO_STYLES,
    generate,
)
from bot_face.renderers.svg import render_svg


def test_render_svg_valid_xml() -> None:
    bot = generate(seed="valid_xml_test", size=256)
    svg_str = bot.to_svg()

    assert svg_str.startswith("<svg")
    assert svg_str.strip().endswith("</svg>")
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg_str
    assert 'viewBox="0 0 256 256"' in svg_str

    # Parse XML to verify well-formed syntax
    root = ET.fromstring(svg_str)
    assert root.tag.endswith("svg")


def test_svg_circle_clip() -> None:
    bot = generate(seed="circle_test", circle=True)
    svg_str = bot.to_svg()
    assert '<circle cx="128" cy="128" r="128"' in svg_str


def test_svg_corner_radius_clip() -> None:
    bot = generate(seed="rounded_test", size=256, corner_radius=32)
    svg_str = bot.to_svg()
    assert 'rx="32" ry="32"' in svg_str


def test_svg_sharp_corners_clip() -> None:
    bot = generate(seed="sharp_test", size=256, corner_radius=0, circle=False)
    svg_str = bot.to_svg()
    assert '<rect x="0" y="0" width="256" height="256"' in svg_str


def test_all_anatomy_combinations_render_valid_svg() -> None:
    # Test all head styles
    for h in HEAD_STYLES:
        b = generate(seed=f"head_{h}")
        b.anatomy.head_style = h
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all faceplate styles
    for f in FACEPLATE_STYLES:
        b = generate(seed=f"face_{f}")
        b.anatomy.faceplate_style = f
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all eye styles
    for e in ALL_EYE_STYLES:
        b = generate(seed=f"eye_{e}")
        b.anatomy.eye_style = e
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all mouth styles
    for m in MOUTH_STYLES:
        b = generate(seed=f"mouth_{m}")
        b.anatomy.mouth_style = m
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all antenna styles
    for a in ANTENNA_STYLES:
        b = generate(seed=f"ant_{a}")
        b.anatomy.antenna_style = a
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all hat styles
    for ht in ALL_HAT_STYLES:
        b = generate(seed=f"hat_{ht}")
        b.anatomy.hat_style = ht
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all badge styles
    for bg in ALL_BADGE_STYLES:
        b = generate(seed=f"badge_{bg}")
        b.anatomy.badge_style = bg
        svg = render_svg(b)
        ET.fromstring(svg)

    # Test all torso styles
    for t in TORSO_STYLES:
        b = generate(seed=f"torso_{t}")
        b.anatomy.torso_style = t
        svg = render_svg(b)
        ET.fromstring(svg)

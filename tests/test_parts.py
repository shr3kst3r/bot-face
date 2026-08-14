"""Comprehensive tests for raster and svg rendering of all individual parts."""

from __future__ import annotations

from bot_face.generator import (
    ALL_BADGE_STYLES,
    ALL_EYE_STYLES,
    ALL_HAT_STYLES,
    ANTENNA_STYLES,
    CHEEK_STYLES,
    EAR_DETAILS,
    FACEPLATE_STYLES,
    FOREHEAD_DETAILS,
    HEAD_STYLES,
    MOUTH_STYLES,
    TORSO_STYLES,
    generate,
)
from bot_face.parts.backgrounds import get_clip_dimensions


def test_get_clip_dimensions() -> None:
    bot = generate(size=256, corner_radius=32, circle=False)
    size, radius, circle = get_clip_dimensions(bot)
    assert size == 256
    assert radius == 32
    assert circle is False

    bot_clamped = generate(size=100, corner_radius=90, circle=False)
    _, radius_clamped, _ = get_clip_dimensions(bot_clamped)
    assert radius_clamped == 50


def test_all_raster_anatomy_combinations() -> None:
    # Render all head styles in raster
    for h in HEAD_STYLES:
        b = generate(seed=f"raster_head_{h}")
        b.anatomy.head_style = h
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all faceplate styles in raster
    for f in FACEPLATE_STYLES:
        b = generate(seed=f"raster_face_{f}")
        b.anatomy.faceplate_style = f
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all eye styles in raster
    for e in ALL_EYE_STYLES:
        b = generate(seed=f"raster_eye_{e}")
        b.anatomy.eye_style = e
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all mouth styles in raster
    for m in MOUTH_STYLES:
        b = generate(seed=f"raster_mouth_{m}")
        b.anatomy.mouth_style = m
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all antenna styles in raster
    for a in ANTENNA_STYLES:
        b = generate(seed=f"raster_ant_{a}")
        b.anatomy.antenna_style = a
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all hat styles in raster
    for ht in ALL_HAT_STYLES:
        b = generate(seed=f"raster_hat_{ht}")
        b.anatomy.hat_style = ht
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all badge styles in raster
    for bg in ALL_BADGE_STYLES:
        b = generate(seed=f"raster_badge_{bg}")
        b.anatomy.badge_style = bg
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all cheek styles in raster & svg
    for ck in CHEEK_STYLES:
        b = generate(seed=f"raster_cheek_{ck}")
        b.anatomy.cheek_style = ck
        img = b.to_image()
        assert img.size == (256, 256)
        svg = b.to_svg()
        assert "<svg" in svg

    # Render ear & forehead details
    for ear in EAR_DETAILS:
        b = generate(seed=f"raster_ear_{ear}")
        b.anatomy.ear_detail = ear
        img = b.to_image()
        assert img.size == (256, 256)

    for fh in FOREHEAD_DETAILS:
        b = generate(seed=f"raster_fh_{fh}")
        b.anatomy.forehead_detail = fh
        img = b.to_image()
        assert img.size == (256, 256)

    # Render all torso styles in raster
    for t in TORSO_STYLES:
        b = generate(seed=f"raster_torso_{t}")
        b.anatomy.torso_style = t
        img = b.to_image()
        assert img.size == (256, 256)

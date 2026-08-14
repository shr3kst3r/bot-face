"""Pillow-based raster avatar renderer supporting anti-aliased PNG/WebP generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from bot_face.parts.accessories import render_raster_cheeks, render_raster_hat
from bot_face.parts.antennae import render_raster_antenna
from bot_face.parts.backgrounds import render_raster_background
from bot_face.parts.bodies import render_raster_body
from bot_face.parts.eyes import render_raster_eyes
from bot_face.parts.heads import render_raster_head
from bot_face.parts.mouths import render_raster_mouth

if TYPE_CHECKING:
    from bot_face.models import RobotAvatar


def render_pillow_image(avatar: RobotAvatar) -> Image.Image:
    """Render a RobotAvatar to a Pillow RGBA Image with smooth corner clipping."""
    target_size = avatar.config.size
    # Use 2x or 4x supersampling for high-quality anti-aliasing
    supersample = 4 if target_size <= 256 else 2
    render_dim = 256 * supersample
    scale = supersample

    # RGBA canvas
    canvas = Image.new("RGBA", (render_dim, render_dim), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # 1. Background
    render_raster_background(draw, avatar, scale=scale)

    # 2. Antenna
    render_raster_antenna(draw, avatar, scale=scale)

    # 3. Body (Neck, Torso, Chest Badge)
    render_raster_body(draw, avatar, scale=scale)

    # 4. Head & Faceplate
    render_raster_head(draw, avatar, scale=scale)

    # 5. Eyes & Eyewear
    render_raster_eyes(draw, avatar, scale=scale)

    # 6. Cheeks
    render_raster_cheeks(draw, avatar, scale=scale)

    # 7. Mouth
    render_raster_mouth(draw, avatar, scale=scale)

    # 8. Hat
    render_raster_hat(draw, avatar, scale=scale)

    # Apply corner clipping mask
    mask = Image.new("L", (render_dim, render_dim), 0)
    mask_draw = ImageDraw.Draw(mask)

    if avatar.config.circle:
        mask_draw.ellipse([(0, 0), (render_dim - 1, render_dim - 1)], fill=255)
    elif avatar.config.corner_radius > 0:
        # Scale corner radius to render dimensions
        radius_ratio = avatar.config.corner_radius / avatar.config.size
        scaled_radius = round(radius_ratio * render_dim)
        max_radius = render_dim // 2
        clamped_radius = min(scaled_radius, max_radius)
        mask_draw.rounded_rectangle(
            [(0, 0), (render_dim - 1, render_dim - 1)],
            radius=clamped_radius,
            fill=255,
        )
    else:
        mask_draw.rectangle([(0, 0), (render_dim - 1, render_dim - 1)], fill=255)

    canvas.putalpha(mask)

    # Resize to final requested dimensions with Lanczos filtering
    if (render_dim, render_dim) != (target_size, target_size):
        return canvas.resize((target_size, target_size), Image.Resampling.LANCZOS)

    return canvas

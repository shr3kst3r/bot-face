"""Native vector SVG avatar renderer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from bot_face.parts.accessories import render_svg_cheeks, render_svg_hat
from bot_face.parts.antennae import render_svg_antenna
from bot_face.parts.backgrounds import render_svg_background
from bot_face.parts.bodies import render_svg_body
from bot_face.parts.eyes import render_svg_eyes
from bot_face.parts.heads import render_svg_head
from bot_face.parts.mouths import render_svg_mouth

if TYPE_CHECKING:
    from bot_face.models import RobotAvatar


def render_svg(avatar: RobotAvatar) -> str:
    """Render a RobotAvatar to a standalone, valid SVG string."""
    size = avatar.config.size
    vb = avatar.viewbox_size

    lines: list[str] = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}" '
            f'width="{size}" height="{size}">'
        ),
        render_svg_background(avatar),
        '  <g clip-path="url(#avatar-clip)">',
    ]

    # Layers ordered from back to front:
    antenna_svg = render_svg_antenna(avatar)
    if antenna_svg:
        lines.append(antenna_svg)

    lines.append(render_svg_body(avatar))
    lines.append(render_svg_head(avatar))
    lines.append(render_svg_eyes(avatar))

    cheeks_svg = render_svg_cheeks(avatar)
    if cheeks_svg:
        lines.append(cheeks_svg)

    lines.append(render_svg_mouth(avatar))

    hat_svg = render_svg_hat(avatar)
    if hat_svg:
        lines.append(hat_svg)

    lines.append("  </g>")
    lines.append("</svg>")
    lines.append("")

    return "\n".join(lines)

"""Data models and avatar representation for bot-face."""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from bot_face.colors import ColorPalette
from bot_face.config import AvatarConfig

if TYPE_CHECKING:
    from PIL import Image


class RobotAnatomy(BaseModel):
    """Anatomy features sampled for a cute robot."""

    head_style: str
    faceplate_style: str
    eye_style: str
    mouth_style: str
    antenna_style: str
    torso_style: str
    badge_style: str
    hat_style: str
    cheek_style: str
    background_style: str
    ear_detail: str
    forehead_detail: str


class RobotAvatar(BaseModel):
    """Generated robot avatar holding all parametric properties and rendering methods."""

    seed: Any
    config: AvatarConfig
    palette: ColorPalette
    anatomy: RobotAnatomy
    viewbox_size: int = Field(default=256, description="Internal vector grid coordinate size")

    model_config = {"arbitrary_types_allowed": True}

    def to_svg(self) -> str:
        """Render the avatar to a valid standalone SVG XML string."""
        from bot_face.renderers.svg import render_svg

        return render_svg(self)

    def to_image(self) -> Image.Image:
        """Render the avatar to a Pillow RGBA Image."""
        from bot_face.filters import apply_filter
        from bot_face.renderers.raster import render_pillow_image

        raw_img = render_pillow_image(self)
        return apply_filter(raw_img, self.config.filter)

    def to_bytes(self, format: str = "png") -> bytes:
        """Render the avatar to encoded image bytes (png, svg, webp, jpeg)."""
        fmt = format.lower().strip().lstrip(".")
        if fmt == "svg":
            return self.to_svg().encode("utf-8")

        img = self.to_image()
        buf = BytesIO()
        if fmt == "jpg":
            fmt = "jpeg"
        # Convert RGBA to RGB for JPEG
        if fmt == "jpeg":
            bg = img.convert("RGB")
            bg.save(buf, format="JPEG", quality=95)
        else:
            img.save(buf, format=fmt.upper())
        return buf.getvalue()

    def to_data_uri(self, format: str = "svg") -> str:
        """Return a data: URI string suitable for inline HTML/CSS <img> src tags."""
        fmt = format.lower().strip().lstrip(".")
        if fmt == "svg":
            encoded = base64.b64encode(self.to_svg().encode("utf-8")).decode("ascii")
            return f"data:image/svg+xml;base64,{encoded}"
        img_bytes = self.to_bytes(fmt)
        encoded = base64.b64encode(img_bytes).decode("ascii")
        mime = f"image/{fmt}" if fmt != "jpg" else "image/jpeg"
        return f"data:{mime};base64,{encoded}"

    def save(self, path: str | Path, format: str | None = None) -> Path:
        """Save the avatar to a file on disk.

        Format is inferred from file extension if not explicitly provided.
        Supported formats: .svg, .png, .webp, .jpg/.jpeg.
        """
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        fmt = format or target.suffix.lstrip(".").lower()
        if not fmt:
            fmt = "png"
            target = target.with_suffix(".png")

        if fmt == "svg":
            target.write_text(self.to_svg(), encoding="utf-8")
        else:
            img_bytes = self.to_bytes(fmt)
            target.write_bytes(img_bytes)

        return target

    def _repr_svg_(self) -> str:
        """Jupyter/IPython rich SVG display support."""
        return self.to_svg()

    def _repr_png_(self) -> bytes:
        """Jupyter/IPython rich PNG display support."""
        return self.to_bytes("png")

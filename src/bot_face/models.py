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
    has_whiskers: bool = False


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

    def to_html_img(
        self,
        alt: str = "Robot Avatar",
        class_name: str = "bot-face-avatar",
        format: str = "svg",
    ) -> str:
        """Return an HTML <img> tag with self-contained data: URI src."""
        uri = self.to_data_uri(format=format)
        size = self.config.size
        return (
            f'<img src="{uri}" alt="{alt}" class="{class_name}" width="{size}" height="{size}" />'
        )

    def to_react_component(self, component_name: str = "BotAvatar") -> str:
        """Return a clean, ready-to-paste React JSX SVG component string."""
        svg = self.to_svg().strip()
        lines = [
            'import React from "react";',
            "",
            f"export const {component_name} = (props: React.SVGProps<SVGSVGElement>) => (",
            f"  {svg}",
            ");",
            "",
            f"export default {component_name};",
            "",
        ]
        return "\n".join(lines)

    def save_iconset(self, output_dir: str | Path) -> dict[str, Path]:
        """Generate a complete web favicon & app icon suite into output_dir.

        Creates:
          - favicon.ico (multi-resolution 16x16, 32x32, 48x48)
          - favicon-16x16.png, favicon-32x32.png
          - apple-touch-icon.png (180x180)
          - android-chrome-192x192.png, android-chrome-512x512.png
          - avatar.svg
          - site.webmanifest
          - html_snippet.html
        """
        from PIL import Image

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        img_512 = self.to_image().resize((512, 512), Image.Resampling.LANCZOS)
        results: dict[str, Path] = {}

        # 1. Favicon .ico (multi-resolution)
        ico_path = out / "favicon.ico"
        img_512.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
        results["favicon.ico"] = ico_path

        # 2. PNG resolutions
        sizes = {
            "favicon-16x16.png": 16,
            "favicon-32x32.png": 32,
            "apple-touch-icon.png": 180,
            "android-chrome-192x192.png": 192,
            "android-chrome-512x512.png": 512,
        }
        for name, dim in sizes.items():
            p = out / name
            resized = img_512.resize((dim, dim), Image.Resampling.LANCZOS)
            resized.save(p, format="PNG")
            results[name] = p

        # 3. Vector SVG
        svg_path = out / "avatar.svg"
        svg_path.write_text(self.to_svg(), encoding="utf-8")
        results["avatar.svg"] = svg_path

        # 4. site.webmanifest
        manifest_path = out / "site.webmanifest"
        manifest_content = (
            "{\n"
            '  "name": "Bot Face Avatar",\n'
            '  "short_name": "Avatar",\n'
            '  "icons": [\n'
            "    {\n"
            '      "src": "/android-chrome-192x192.png",\n'
            '      "sizes": "192x192",\n'
            '      "type": "image/png"\n'
            "    },\n"
            "    {\n"
            '      "src": "/android-chrome-512x512.png",\n'
            '      "sizes": "512x512",\n'
            '      "type": "image/png"\n'
            "    }\n"
            "  ],\n"
            f'  "theme_color": "{self.palette.background}",\n'
            f'  "background_color": "{self.palette.background}",\n'
            '  "display": "standalone"\n'
            "}\n"
        )
        manifest_path.write_text(manifest_content, encoding="utf-8")
        results["site.webmanifest"] = manifest_path

        # 5. HTML snippet
        html_path = out / "html_snippet.html"
        html_content = (
            '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n'
            '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
            '<link rel="manifest" href="/site.webmanifest">\n'
        )
        html_path.write_text(html_content, encoding="utf-8")
        results["html_snippet.html"] = html_path

        return results

    def _repr_svg_(self) -> str:
        """Jupyter/IPython rich SVG display support."""
        return self.to_svg()

    def _repr_png_(self) -> bytes:
        """Jupyter/IPython rich PNG display support."""
        return self.to_bytes("png")

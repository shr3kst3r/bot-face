"""Image filters and retro style transformations (8-bit, 16-bit, Game Boy, CRT, etc.)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

if TYPE_CHECKING:
    pass

AVAILABLE_FILTERS: dict[str, str] = {
    "8bit": "Classic chunky 8-bit retro arcade / NES pixel art style",
    "16bit": "16-bit SNES / Genesis arcade pixel art style with dithering",
    "gameboy": "Classic 4-shade olive green Nintendo Game Boy DMG-01 LCD screen",
    "crt": "Retro arcade CRT television monitor with horizontal scanlines",
    "blueprint": "Technical cyan/navy architectural blueprint style",
    "monochrome": "High-contrast clean black & white grayscale",
    "sepia": "Warm nostalgic vintage photograph tone",
    "dither": "Floyd-Steinberg 1-bit dot-matrix dither",
    "neon_glow": "Vibrant cyberpunk neon bloom and color saturation boost",
}

# 4 classic Game Boy DMG-01 palette colors (darkest to lightest)
GAMEBOY_PALETTE = [
    (15, 56, 15),  # #0F380F
    (48, 98, 48),  # #306230
    (139, 172, 15),  # #8BAC0F
    (155, 188, 15),  # #9BBC0F
]


def list_filters() -> list[str]:
    """Return a sorted list of available filter names."""
    return sorted(AVAILABLE_FILTERS.keys())


def apply_8bit_filter(img: Image.Image) -> Image.Image:
    """Transform image into chunky 8-bit pixel art with 16-color quantization."""
    orig_w, orig_h = img.size
    grid_size = 32

    # Separate alpha channel
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Downscale RGB with box sampling
    small_rgb = rgb.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    # Quantize to 16 colors
    quantized = small_rgb.quantize(colors=16, method=Image.Quantize.MEDIANCUT).convert("RGB")
    # Upscale back to original dimensions with nearest neighbor
    pixelated_rgb = quantized.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    # Downscale & upscale alpha with nearest neighbor to preserve crisp pixel edges
    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    pr, pg, pb = pixelated_rgb.split()
    return Image.merge("RGBA", (pr, pg, pb, pixelated_a))


def apply_16bit_filter(img: Image.Image) -> Image.Image:
    """Transform image into 16-bit arcade pixel art with 64-color dithering."""
    orig_w, orig_h = img.size
    grid_size = 64

    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    small_rgb = rgb.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    quantized = small_rgb.quantize(
        colors=64,
        method=Image.Quantize.MAXCOVERAGE,
        dither=Image.Dither.FLOYDSTEINBERG,
    ).convert("RGB")
    pixelated_rgb = quantized.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    pr, pg, pb = pixelated_rgb.split()
    return Image.merge("RGBA", (pr, pg, pb, pixelated_a))


def apply_gameboy_filter(img: Image.Image) -> Image.Image:
    """Transform image into authentic 4-color Game Boy LCD screen pixel art."""
    orig_w, orig_h = img.size
    grid_size = 36

    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Convert to grayscale and downscale
    gray = ImageOps.grayscale(rgb)
    small_gray = gray.resize((grid_size, grid_size), Image.Resampling.BILINEAR)

    # Map grayscale [0..255] into 4 Game Boy palette colors
    out_rgb = Image.new("RGB", (grid_size, grid_size))
    for y in range(grid_size):
        for x in range(grid_size):
            pixel_val = small_gray.getpixel((x, y))
            val = int(pixel_val) if isinstance(pixel_val, (int, float)) else 0
            idx = min(3, max(0, val // 64))
            out_rgb.putpixel((x, y), GAMEBOY_PALETTE[idx])

    pixelated_rgb = out_rgb.resize((orig_w, orig_h), Image.Resampling.NEAREST)
    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    pr, pg, pb = pixelated_rgb.split()
    return Image.merge("RGBA", (pr, pg, pb, pixelated_a))


def apply_crt_filter(img: Image.Image) -> Image.Image:
    """Apply retro arcade CRT scanline and phosphor bloom filter."""
    rgba = img.convert("RGBA")
    w, h = rgba.size

    # Create scanlines overlay
    scanlines = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(scanlines)
    for y in range(0, h, 3):
        s_draw.line([(0, y), (w, y)], fill=(0, 0, 0, 70), width=1)

    # Slight bloom
    bloom = rgba.filter(ImageFilter.GaussianBlur(radius=2))
    enhanced = Image.blend(rgba, bloom, alpha=0.25)

    # Composite scanlines
    result = Image.alpha_composite(enhanced, scanlines)
    # Restore original alpha
    result.putalpha(rgba.split()[3])
    return result


def apply_blueprint_filter(img: Image.Image) -> Image.Image:
    """Transform avatar into an architectural cyan blueprint style."""
    rgba = img.convert("RGBA")
    w, h = rgba.size
    alpha = rgba.split()[3]

    gray = ImageOps.grayscale(img.convert("RGB"))
    # Invert and boost contrast for line art look
    inv = ImageOps.invert(gray)
    enhancer = ImageEnhance.Contrast(inv)
    high_contrast = enhancer.enhance(1.8)

    # Colorize onto navy background (#0D1B2A) with cyan lines (#00E5FF)
    blueprint_rgb = ImageOps.colorize(
        high_contrast,
        black=(13, 27, 42),
        white=(0, 229, 255),
        mid=(0, 119, 182),
    )

    # Grid overlay
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid)
    grid_spacing = max(8, w // 16)
    for x in range(0, w, grid_spacing):
        g_draw.line([(x, 0), (x, h)], fill=(0, 229, 255, 30), width=1)
    for y in range(0, h, grid_spacing):
        g_draw.line([(0, y), (w, y)], fill=(0, 229, 255, 30), width=1)

    bp_rgba = blueprint_rgb.convert("RGBA")
    combined = Image.alpha_composite(bp_rgba, grid)
    combined.putalpha(alpha)
    return combined


def apply_monochrome_filter(img: Image.Image) -> Image.Image:
    """Transform avatar into high-contrast black and white."""
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    gray = ImageOps.grayscale(rgba.convert("RGB"))
    enhancer = ImageEnhance.Contrast(gray)
    boosted = enhancer.enhance(1.3)
    mono_rgb = boosted.convert("RGB")
    r, g, b = mono_rgb.split()
    return Image.merge("RGBA", (r, g, b, alpha))


def apply_sepia_filter(img: Image.Image) -> Image.Image:
    """Transform avatar into a warm nostalgic sepia tone."""
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    gray = ImageOps.grayscale(rgba.convert("RGB"))
    sepia_rgb = ImageOps.colorize(
        gray,
        black=(34, 18, 5),
        white=(255, 240, 200),
        mid=(140, 100, 60),
    )
    r, g, b = sepia_rgb.split()
    return Image.merge("RGBA", (r, g, b, alpha))


def apply_dither_filter(img: Image.Image) -> Image.Image:
    """Apply 1-bit Floyd-Steinberg dot-matrix dithering."""
    orig_w, orig_h = img.size
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    gray = ImageOps.grayscale(rgba.convert("RGB"))
    small_gray = gray.resize((128, 128), Image.Resampling.BILINEAR)
    dithered = small_gray.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
    dithered_full = dithered.resize((orig_w, orig_h), Image.Resampling.NEAREST).convert("RGB")
    r, g, b = dithered_full.split()
    return Image.merge("RGBA", (r, g, b, alpha))


def apply_neon_glow_filter(img: Image.Image) -> Image.Image:
    """Apply intense cyberpunk neon color saturation and bloom glow."""
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    # Color saturation boost
    color_enhancer = ImageEnhance.Color(rgba)
    saturated = color_enhancer.enhance(1.8)
    contrast_enhancer = ImageEnhance.Contrast(saturated)
    boosted = contrast_enhancer.enhance(1.2)

    # Bloom blur layer
    bloom = boosted.filter(ImageFilter.GaussianBlur(radius=4))
    glow_combined = Image.blend(boosted, bloom, alpha=0.3)
    glow_combined.putalpha(alpha)
    return glow_combined


FILTER_FUNCTIONS = {
    "8bit": apply_8bit_filter,
    "16bit": apply_16bit_filter,
    "gameboy": apply_gameboy_filter,
    "crt": apply_crt_filter,
    "blueprint": apply_blueprint_filter,
    "monochrome": apply_monochrome_filter,
    "grayscale": apply_monochrome_filter,
    "sepia": apply_sepia_filter,
    "dither": apply_dither_filter,
    "neon_glow": apply_neon_glow_filter,
    "neon": apply_neon_glow_filter,
}


def apply_filter(img: Image.Image, filter_name: str | None) -> Image.Image:
    """Apply a named retro look or image filter to a Pillow Image."""
    if not filter_name or filter_name.lower() in ("none", "raw", "plain"):
        return img

    norm_name = filter_name.lower().replace("-", "_").strip()
    if norm_name not in FILTER_FUNCTIONS:
        valid = ", ".join(sorted(AVAILABLE_FILTERS.keys()))
        msg = f"Unknown filter '{filter_name}'. Available filters: {valid}"
        raise ValueError(msg)

    return FILTER_FUNCTIONS[norm_name](img)

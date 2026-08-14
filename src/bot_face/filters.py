"""Image filters and retro style transformations (8-bit, 16-bit, Game Boy, CRT, etc.)."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

AVAILABLE_FILTERS: dict[str, str] = {
    "8bit": "Classic chunky 8-bit retro arcade / NES pixel art style with bold outlines",
    "16bit": "16-bit SNES / Genesis arcade pixel art style with dithering and outline retention",
    "gameboy": "Classic 4-shade olive green Nintendo Game Boy DMG-01 LCD screen with dark outlines",
    "crt": "Retro arcade CRT television monitor with horizontal scanlines",
    "blueprint": "Technical cyan/navy architectural blueprint style",
    "monochrome": "High-contrast clean black & white grayscale",
    "sepia": "Warm nostalgic vintage photograph tone",
    "dither": "Floyd-Steinberg 1-bit dot-matrix dither",
    "neon_glow": "Vibrant cyberpunk neon bloom and color saturation boost",
}

# 4 classic Game Boy DMG-01 palette colors (darkest to lightest)
GAMEBOY_PALETTE = [
    (15, 56, 15),  # #0F380F (deepest dark green - outline / dark shadow)
    (48, 98, 48),  # #306230 (dark olive green - shadow / accents)
    (139, 172, 15),  # #8BAC0F (mid lime green - chassis / midtones)
    (155, 188, 15),  # #9BBC0F (light greenish yellow - background / highlights)
]


def _safe_rgba(val: object) -> tuple[int, int, int, int]:
    """Safely convert any PIL getpixel return value into an RGBA 4-tuple."""
    if isinstance(val, (tuple, list)):
        r = int(val[0])
        g = int(val[1]) if len(val) > 1 else r
        b = int(val[2]) if len(val) > 2 else r
        a = int(val[3]) if len(val) > 3 else 255
        return (r, g, b, a)
    num = int(val) if isinstance(val, (int, float)) else 0
    return (num, num, num, 255)


def list_filters() -> list[str]:
    """Return a sorted list of available filter names."""
    return sorted(AVAILABLE_FILTERS.keys())


def apply_8bit_filter(img: Image.Image) -> Image.Image:
    """Transform image into 8-bit pixel art with 16-color quantization and outlines."""
    orig_w, orig_h = img.size
    grid_size = 48

    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Detect dark lines and contours in high-res
    gray = ImageOps.grayscale(rgb)
    dark_mask = gray.point(lambda p: 255 if p < 70 else 0, mode="1")
    small_dark = dark_mask.resize((grid_size, grid_size), Image.Resampling.NEAREST)

    small_rgb = rgb.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    quantized_rgb = small_rgb.quantize(
        colors=16, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG
    ).convert("RGB")

    # Enforce crisp dark outlines
    for y in range(grid_size):
        for x in range(grid_size):
            if small_dark.getpixel((x, y)):
                quantized_rgb.putpixel((x, y), (20, 20, 30))

    pixelated_rgb = quantized_rgb.resize((orig_w, orig_h), Image.Resampling.NEAREST)
    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    pr, pg, pb = pixelated_rgb.split()
    return Image.merge("RGBA", (pr, pg, pb, pixelated_a))


def apply_16bit_filter(img: Image.Image) -> Image.Image:
    """Transform image into 16-bit SNES arcade pixel art with dithering and outlines."""
    orig_w, orig_h = img.size
    grid_size = 64

    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Detect dark contours
    gray = ImageOps.grayscale(rgb)
    dark_mask = gray.point(lambda p: 255 if p < 70 else 0, mode="1")
    small_dark = dark_mask.resize((grid_size, grid_size), Image.Resampling.NEAREST)

    small_rgb = rgb.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    quantized_rgb = small_rgb.quantize(
        colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG
    ).convert("RGB")

    for y in range(grid_size):
        for x in range(grid_size):
            if small_dark.getpixel((x, y)):
                quantized_rgb.putpixel((x, y), (15, 15, 25))

    pixelated_rgb = quantized_rgb.resize((orig_w, orig_h), Image.Resampling.NEAREST)
    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)

    pr, pg, pb = pixelated_rgb.split()
    return Image.merge("RGBA", (pr, pg, pb, pixelated_a))


def apply_gameboy_filter(img: Image.Image) -> Image.Image:
    """Transform image into authentic 4-color Game Boy LCD pixel art with bold dark outlines."""
    orig_w, orig_h = img.size
    grid_size = 64
    small_raw = img.resize((grid_size, grid_size), Image.Resampling.BILINEAR)

    # Detect background pixels by sampling the four corners
    c00 = _safe_rgba(small_raw.getpixel((0, 0)))
    c10 = _safe_rgba(small_raw.getpixel((grid_size - 1, 0)))
    c01 = _safe_rgba(small_raw.getpixel((0, grid_size - 1)))
    c11 = _safe_rgba(small_raw.getpixel((grid_size - 1, grid_size - 1)))
    corners = [c00, c10, c01, c11]

    is_bg = [[False] * grid_size for _ in range(grid_size)]
    for y in range(grid_size):
        for x in range(grid_size):
            p = _safe_rgba(small_raw.getpixel((x, y)))
            if p[3] < 128:
                is_bg[y][x] = True
            else:
                for c in corners:
                    dr = abs(p[0] - c[0])
                    dg = abs(p[1] - c[1])
                    db = abs(p[2] - c[2])
                    if dr + dg + db < 35:
                        is_bg[y][x] = True
                        break

    # Determine character silhouette boundary pixels
    is_border = [[False] * grid_size for _ in range(grid_size)]
    for y in range(grid_size):
        for x in range(grid_size):
            if not is_bg[y][x]:
                for dy, dx in [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1),
                    (-1, -1),
                    (-1, 1),
                    (1, -1),
                    (1, 1),
                ]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < grid_size and 0 <= nx < grid_size and is_bg[ny][nx]:
                        is_border[y][x] = True
                        break

    gray = ImageOps.grayscale(small_raw)
    char_gray = ImageOps.autocontrast(gray, cutoff=2)

    out_img = Image.new("RGB", (grid_size, grid_size))
    for y in range(grid_size):
        for x in range(grid_size):
            if is_bg[y][x]:
                # Light green Game Boy LCD screen background (shade 3)
                out_img.putpixel((x, y), GAMEBOY_PALETTE[3])
            elif is_border[y][x]:
                # Deepest dark green silhouette outline (shade 0)
                out_img.putpixel((x, y), GAMEBOY_PALETTE[0])
            else:
                raw_g = char_gray.getpixel((x, y))
                g = int(raw_g) if isinstance(raw_g, (int, float)) else 0
                if g < 60:
                    out_img.putpixel((x, y), GAMEBOY_PALETTE[0])
                elif g < 120:
                    out_img.putpixel((x, y), GAMEBOY_PALETTE[1])
                elif g < 185:
                    out_img.putpixel((x, y), GAMEBOY_PALETTE[2])
                else:
                    out_img.putpixel((x, y), GAMEBOY_PALETTE[3])

    out = out_img.resize((orig_w, orig_h), Image.Resampling.NEAREST)
    rgba = img.convert("RGBA")
    _, _, _, a = rgba.split()
    small_a = a.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    pixelated_a = small_a.resize((orig_w, orig_h), Image.Resampling.NEAREST)
    pr, pg, pb = out.split()
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
    enhanced.paste(scanlines, (0, 0), scanlines)
    return enhanced


def apply_blueprint_filter(img: Image.Image) -> Image.Image:
    """Transform image into architectural cyan/navy blueprint line art."""
    rgba = img.convert("RGBA")
    orig_w, orig_h = rgba.size
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Convert to grayscale and find edges
    gray = ImageOps.grayscale(rgb)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges_inv = ImageOps.invert(edges)

    # Create navy blueprint background
    blueprint = Image.new("RGB", (orig_w, orig_h), (10, 25, 47))
    b_draw = ImageDraw.Draw(blueprint)

    # Subtle grid lines
    for x in range(0, orig_w, 16):
        b_draw.line([(x, 0), (x, orig_h)], fill=(20, 45, 75), width=1)
    for y in range(0, orig_h, 16):
        b_draw.line([(0, y), (orig_w, y)], fill=(20, 45, 75), width=1)

    # Colorize inverted edges in electric cyan
    cyan_lines = ImageOps.colorize(edges_inv, black="#00F5D4", white="#0A192F")
    result = Image.blend(blueprint, cyan_lines, alpha=0.85)

    res_r, res_g, res_b = result.split()
    return Image.merge("RGBA", (res_r, res_g, res_b, a))


def apply_monochrome_filter(img: Image.Image) -> Image.Image:
    """Convert avatar to high-contrast clean black & white grayscale."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    gray = ImageOps.grayscale(rgb)
    contrasted = ImageEnhance.Contrast(gray).enhance(1.4)
    rgb_gray = contrasted.convert("RGB")
    gr, gg, gb = rgb_gray.split()
    return Image.merge("RGBA", (gr, gg, gb, a))


def apply_sepia_filter(img: Image.Image) -> Image.Image:
    """Apply warm vintage sepia photograph tone."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    gray = ImageOps.grayscale(rgb)
    sepia_rgb = ImageOps.colorize(gray, black="#2C1608", white="#FFF4D6")
    sr, sg, sb = sepia_rgb.split()
    return Image.merge("RGBA", (sr, sg, sb, a))


def apply_dither_filter(img: Image.Image) -> Image.Image:
    """Apply 1-bit Floyd-Steinberg dot-matrix dithering."""
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()
    rgb = Image.merge("RGB", (r, g, b))

    gray = ImageOps.grayscale(rgb)
    contrasted = ImageEnhance.Contrast(gray).enhance(1.3)
    dithered = contrasted.convert("1", dither=Image.Dither.FLOYDSTEINBERG).convert("RGBA")
    dr, dg, db, _ = dithered.split()
    return Image.merge("RGBA", (dr, dg, db, a))


def apply_neon_glow_filter(img: Image.Image) -> Image.Image:
    """Apply intense cyberpunk bloom and color saturation boost."""
    rgba = img.convert("RGBA")
    enhanced = ImageEnhance.Color(rgba).enhance(1.6)
    enhanced = ImageEnhance.Contrast(enhanced).enhance(1.2)

    bloom = enhanced.filter(ImageFilter.GaussianBlur(radius=4))
    res = Image.blend(enhanced, bloom, alpha=0.35)
    return res


def apply_filter(img: Image.Image, filter_name: str | None) -> Image.Image:
    """Apply the specified filter by name to the image."""
    if filter_name is None or filter_name.lower() in ("none", ""):
        return img

    f_key = filter_name.lower().replace("-", "_").strip()
    if f_key == "8bit":
        return apply_8bit_filter(img)
    if f_key == "16bit":
        return apply_16bit_filter(img)
    if f_key == "gameboy":
        return apply_gameboy_filter(img)
    if f_key == "crt":
        return apply_crt_filter(img)
    if f_key == "blueprint":
        return apply_blueprint_filter(img)
    if f_key == "monochrome":
        return apply_monochrome_filter(img)
    if f_key == "sepia":
        return apply_sepia_filter(img)
    if f_key == "dither":
        return apply_dither_filter(img)
    if f_key == "neon_glow":
        return apply_neon_glow_filter(img)

    available = ", ".join(list_filters())
    msg = f"Unknown filter '{filter_name}'. Available filters: {available}"
    raise ValueError(msg)

<div align="center">

# 🤖 Bot-Face

**A lightweight, zero-system-dependency Python library & CLI for generating cute, expressive robot profile avatars.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg?style=flat)]()
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg?style=flat)]()
[![Type Checked](https://img.shields.io/badge/ty-checked-blue.svg?style=flat)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

*Dual-engine rendering: Native Vector SVG + Pixel-Perfect Pillow Rasterization (PNG/WebP/ICO).*

[**🎨 Explore the Full Visual Gallery (EXAMPLES.md)**](EXAMPLES.md)

</div>

---

## ✨ Features

- **🎨 40 Curated Bright Color Palettes**: Hand-tailored HSL color harmonies with dedicated dark silhouette outlines for maximum legibility on any background.
- **🎭 Mood & Expression Presets**: Emotional presets (`happy`, `cool`, `love`, `surprised`, `wink`, `sleepy`, `neutral`) that coordinate eyes, mouth expressions, cheeks, and accessories.
- **🐾 Animal Robot Modes**: Dedicated animal presets (`--cat`, `--bunny`, `--bear`, or `--animal <name>`) with custom ears, whiskers, bell collars, and chest badges.
- **🔲 Transparent & Custom Backgrounds**: Generate transparent avatar stickers with `--transparent` or customize with `--bg <hex>` for seamless UI integration.
- **💡 3D Cel-Shading & Minimalist Flat Modes**: Toggle between dimensional lighting with specular highlight cuts, chassis shadow bevels, and glass faceplate sheens (`shading=True`) or clean minimalist flat vector illustration (`--no-shading`).
- **📦 Web Icon & Favicon Suite Generator**: Export full multi-resolution favicon suites (`favicon.ico`, `apple-touch-icon.png`, Android Chrome icons, and webmanifest) with one command (`bf iconset` / `avatar.save_iconset()`).
- **🧩 React & HTML Helpers**: Generate self-contained `<img src="data:image/svg+xml;base64,...">` tags (`avatar.to_html_img()`) or React JSX components (`avatar.to_react_component()`).
- **🕹️ Retro Looks & Pixel Art Filters**:
  - `gameboy`: Authentic 4-color olive green Nintendo Game Boy DMG-01 LCD screen with dark outline boundary preservation.
  - `8bit`: Chunky retro arcade / NES 16-color pixel art.
  - `16bit`: Smooth SNES / Genesis pixel art with Floyd-Steinberg error-diffusion dithering.
  - `crt`: Retro arcade CRT television monitor with phosphor scanlines and bloom glow.
  - `blueprint`: Architectural cyan & navy engineering schematic.
  - `neon_glow`: Cyberpunk bloom with high saturation.
  - `sepia`: Nostalgic 19th-century vintage photograph look.
  - `dither`: 1-bit monochrome terminal dot-matrix dither.
- **🎲 Deterministic Seeding**: Pass any seed string (usernames, email addresses, UUIDs) or raw bytes to deterministically reproduce the exact same robot every time. Random generation supported on demand.
- **🔲 Flexible Geometry & Clipping**: Sharp square, smooth rounded rectangles (`--radius <px>`), or perfect circular profile clips (`--circle`).
- **🚀 Dual Output Engine**: Zero external C/Rust binary dependencies (no Cairo or libxml required). Generates standard SVG strings or rasterizes via Pillow into anti-aliased PNG, WebP, ICO, or base64 Data URIs.

---

## 📦 Installation

```bash
# Using pip
pip install bot-face

# Using uv
uv add bot-face
```

---

## 🚀 Quickstart

### 1. Python Library

```python
import bot_face

# --- Simple Direct Helpers ---
# Generate standalone SVG XML string
svg_markup = bot_face.render_svg(seed="alice@example.com", size=256, corner_radius=32)

# Generate raw PNG bytes (circular profile avatar with transparent background)
png_bytes = bot_face.render_png(seed="bob@example.com", size=256, circle=True, transparent=True)


# --- Object-Oriented Generator ---
avatar = bot_face.generate(
    seed="octocat_42",
    size=256,
    corner_radius=24,  # 0 for square, >0 for rounded corners
    circle=False,  # Set True for circular profile clip
    palette="bubblegum",  # Explicit palette name (or None for seeded choice)
    mood="love",  # 'happy', 'cool', 'love', 'surprised', 'wink', 'sleepy'
    animal="cat",  # 'cat', 'bunny', 'bear' (or None)
    transparent=False,  # Set True for alpha transparent canvas
    shading=True,  # 3D cel-shading & highlights (False for flat minimalist)
    filter=None,  # Retro filter: '8bit', '16bit', 'gameboy', 'crt', etc.
)

# Save directly to disk (format inferred from file extension)
avatar.save("avatar.png")
avatar.save("avatar.svg")
avatar.save("avatar.webp")

# Generate full web favicon suite (favicon.ico, apple-touch-icon, webmanifest)
icon_files = avatar.save_iconset("./web_icons")

# Ready-to-use HTML <img> tag with data: URI
html_tag = avatar.to_html_img(alt="Profile Picture")

# Clean React JSX component string
react_code = avatar.to_react_component("UserAvatar")
```

---

### 2. Command-Line Interface (`bf` / `bot-face`)

The package exposes both `bot-face` and the shortcut `bf`:

```bash
# Generate avatar for a user seed with rounded corners
bf generate "alice@example.com" --radius 32 --output alice.png

# Generate a love-mood robot cat with heart eyes and bell collar
bf generate "neko_bot" --cat --mood love --palette cotton_candy --output cat.png

# Generate a cute bunny robot with transparent background
bf generate "bunny_bot" --bunny --transparent --output bunny.png

# Generate an authentic Game Boy DMG-01 pixel LCD avatar
bf generate "retro_hero" --filter gameboy --output gameboy.png

# Generate a flat minimalist vector avatar without shading
bf generate "minimalist" --no-shading --output flat.svg

# Generate a complete web favicon & app icon suite
bf iconset "brand_logo" --palette cyber_mint --circle --output-dir ./public/icons

# List all available palettes, filters, and mood presets
bf palettes
bf filters
bf moods

# Output base64 data: URI string for HTML/CSS embedding
bf generate "embed_bot" --data-uri

# Batch generate avatars for an entire list of users
bf batch alice bob charlie dev_ops admin --radius 24 --format png --output-dir ./avatars

# Inspect anatomical breakdown of a seed in the terminal
bf preview "octocat"
```

---

## 🎨 Color Palettes (40 Total)

List all available palettes anytime via `bf palettes`:

| Category | Available Palettes | Description |
|---|---|---|
| 🍬 **Candy & Sweets** | `bubblegum`, `cotton_candy`, `strawberry_matcha`, `peaches_and_cream`, `candy_corn`, `mint_chocolate`, `caramel_latte`, `blueberry_muffin` | Bright candy pinks, vanilla creams, pastel berry reds, and buttery golden tones. |
| ⚡ **Cyberpunk & Arcade** | `cyberpunk_2077`, `cyber_mint`, `arcade_pop`, `tokyo_night`, `synthwave_sunset`, `hyper_lime`, `midnight_prism`, `vaporwave` | High-voltage neon yellows, laser cyans, hot magentas, and deep synthwave purples. |
| 🌌 **Cosmic & Ocean** | `galaxy_nebula`, `abyssal_deep`, `aurora_borealis`, `arctic_fox`, `glacier_ice`, `aqua_splash`, `lavender_sky` | Deep space indigos, polar teals, icy cyans, and celestial periwinkles. |
| ☀️ **Warm & Vibrant** | `sunny_lemon`, `solar_flare`, `sunset_glow`, `lava_magma`, `golden_hour`, `bumblebee`, `neon_coral` | Sunshine yellows, fiery crimson reds, radiant oranges, and warm amber golds. |
| 🌿 **Fresh & Botanical** | `matcha_latte`, `pistachio_cream`, `poison_ivy`, `emerald_bot`, `cherry_blossom`, `dragonfruit`, `tropic_paradise`, `papaya_punch` | Calm matcha greens, cherry sakura pinks, tropical mangoes, and electric limes. |

---

## 🎭 Mood & Expression Presets

List all mood presets via `bf moods`:

| Mood Preset | Visual Expression Focus |
|---|---|
| `happy` | Smiling mouth (`^ ^` or open grin) + rosy blush cheeks. |
| `cool` | Dark sunglasses or cyclops visor + calm smile. |
| `love` | Glowing heart LED matrix eyes (`♥ ♥`) + sweet heart blush + heart chest badge. |
| `surprised` | Wide lens eyes (`O O`) + cute open mouth (`:o`) + lightbulb antenna. |
| `wink` | Playful wink eye + cute cat/vamp mouth + rosy blush. |
| `sleepy` | Half-closed LED dots/slits + oscilloscope snooze wave + dash blush. |
| `neutral` | Glossy pupil lenses + speaker grill mouth. |

---

## 🕹️ Retro & Visual Filters

List all available filters anytime via `bf filters`:

| Filter Name | Aesthetic Description |
|---|---|
| `8bit` | Chunky retro arcade / NES 16-color pixel art with reinforced contours. |
| `16bit` | Smooth 16-bit SNES / Genesis pixel art with Floyd-Steinberg error diffusion dithering. |
| `gameboy` | Authentic 4-color olive green Nintendo Game Boy DMG-01 LCD screen with dark outlines. |
| `crt` | Retro arcade CRT monitor with horizontal scanlines, phosphor bloom, and vignette curvature. |
| `blueprint` | Architectural cyan and navy technical blueprint with inverted line art. |
| `neon_glow` | High-saturation cyberpunk neon glow with bloom radiance. |
| `sepia` | Warm vintage 19th-century photograph tone. |
| `dither` | 1-bit Floyd-Steinberg monochrome dot-matrix halftone printer / terminal dither. |
| `monochrome` | High-contrast black-and-white grayscale. |

---

## 📖 CLI Command Reference

### `bf generate`

```
Usage: bf generate [OPTIONS] [SEED]

Options:
  -o, --output PATH              Output file path (.svg, .png, .webp).
  -f, --format [svg|png|webp]    Explicit output format.
  -s, --size INTEGER             Image width and height in pixels (16 to 4096). [default: 256]
  -r, --radius INTEGER           Corner radius in pixels. [default: 0]
  -c, --circle                   Clip avatar into a circle. [default: False]
  -p, --palette TEXT             Explicit color palette name.
  -F, --filter TEXT              Retro filter: '8bit', '16bit', 'gameboy', 'crt', etc.
  -m, --mood TEXT                Mood preset: 'happy', 'cool', 'love', 'surprised', 'wink', etc.
  -a, --animal [cat|bunny|bear]  Animal robot preset.
  --cat / --no-cat               Force cute cat robot features.
  --bunny                        Force cute bunny robot features.
  --bear                         Force cute bear robot features.
  --transparent                  Render with a transparent background.
  --bg-color, --bg TEXT          Custom background color override (hex).
  --shading / --no-shading       Enable or disable 3D cel-shading. [default: True]
  --hat / --no-hat               Force hat presence or absence.
  --glasses / --no-glasses       Force eyewear presence or absence.
  --badge / --no-badge           Force chest badge presence or absence.
  --random                       Generate with a random cryptographic seed.
  --data-uri                     Output base64 data: URI string for HTML/CSS embedding.
  --help                         Show this message and exit.
```

### `bf iconset`

```
Usage: bf iconset [OPTIONS] SEED

Options:
  -o, --output-dir DIRECTORY     Directory to save web icon suite. [default: ./icons]
  -p, --palette TEXT             Explicit color palette.
  -c, --circle                   Clip icons into a circle.
  --transparent                  Render icons with transparent background.
  -m, --mood TEXT                Mood preset.
  --cat / --no-cat               Force cat robot features.
  --help                         Show this message and exit.
```

### `bf batch`

```
Usage: bf batch [OPTIONS] SEEDS...

Options:
  -o, --output-dir DIRECTORY     Target directory to save avatar images. [default: ./avatars]
  -f, --format [svg|png|webp]    Output file format. [default: png]
  -s, --size INTEGER             Image size in pixels. [default: 256]
  -r, --radius INTEGER           Corner radius in pixels. [default: 0]
  -c, --circle                   Clip avatars to circular profile shape.
  -p, --palette TEXT             Fixed palette name for all avatars.
  -F, --filter TEXT              Retro filter for all avatars.
  -m, --mood TEXT                Mood preset for all avatars.
  --transparent                  Render with transparent background.
  --shading / --no-shading       Enable or disable 3D cel-shading. [default: True]
  --help                         Show this message and exit.
```

---

## 🛠️ Development & Testing

This project is built with modern Python packaging tooling (`uv`, `ruff`, `ty`, `pytest`):

```bash
# Run verification suite (linting, formatting, typechecking, tests)
just verify

# Format codebase
just format

# Run test suite with coverage report
just test
```

---

## 📄 License

MIT License. Designed and crafted with ❤️ for clean, vibrant robot account avatars.
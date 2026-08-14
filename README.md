# 🤖 bot-face

A lightweight, high-performance Python library and CLI for generating bright, cute, customizable robot avatars for user profiles and account images.

[![CI Gate](https://img.shields.io/badge/verify-passing-brightgreen)](justfile)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

- **🎨 Bright & Cheerful Aesthetics**: 12 curated, vibrant color themes (Bubblegum, Cyber Mint, Sunny Lemon, Electric Berry, Neon Coral, and more).
- **🎲 Deterministic & Random Seeding**: Pass any seed (`str`, `int`, `bytes`) to reproduce the exact same avatar every time (ideal for usernames, emails, and UUIDs) or generate random avatars on demand.
- **🔲 Configurable Corner Clipping**: Sharp square, smooth rounded rectangles (`corner_radius=...`), or full circular profile clips (`circle=True`).
- **🎩 Expressive Robot Anatomy**:
  - **Heads**: Curved TV monitors, capsules, retro domes, rounded boxes, robot cat ears, bear ears.
  - **Eyes & Eyewear**: Glossy lens eyes with pupil sparkles, happy LED matrices (`^ ^`, `• •`, `★ ★`, `♥ ♥`), visors, sunglasses, nerdy spectacles, retro goggles.
  - **Mouths**: Happy smiles, cat smiles (`:3`), speaker grills, oscilloscope heartbeat waves, toothy grins, audio VU meters.
  - **Antennae & Gadgets**: Glowing bulbs, dual coils/springs, radar dishes, lightning bolts, siren beacons, headphones/earmuffs.
  - **Accessories & Badges**: Party hats, bowler hats, propeller beanies, crowns, blushing cheeks, hearts, stars, battery meters, power buttons.
- **⚡ Dual Export (Vector & Raster)**:
  - **Pure Vector SVG**: Resolution-independent, lightweight (< 4KB), zero system C dependencies.
  - **Pillow Rasterizer**: High-resolution anti-aliased PNG, WebP, and JPEG rendering with alpha-transparency for rounded corners.
  - **Data URIs**: Base64 data URIs for inline HTML/CSS `<img>` tags.
- **💻 Rich CLI**: Built with Typer and Rich, supporting batch generation, terminal preview, and palette inspection.

---

## 📦 Installation

```bash
# Using uv (recommended)
uv add bot-face

# Using pip
pip install bot-face
```

---

## 🚀 Quickstart

### Python Library

```python
import bot_face

# 1. Direct generation with high-level helpers
svg_data = bot_face.render_svg(seed="alice@example.com", size=256, corner_radius=32)
png_data = bot_face.render_png(seed="alice@example.com", size=256, circle=True)

# 2. Object-oriented API
avatar = bot_face.generate(
    seed="octocat",
    size=256,
    corner_radius=24,      # 0 for square, >0 for rounded
    circle=False,          # Set True for full circle profile image
    palette="cyber_mint",  # Optional explicit palette (or None for seeded choice)
    has_hat=True,          # Optional override for hat presence
    has_glasses=False,     # Optional override for eyewear
    has_badge=True,        # Optional override for chest badge
)

# Save to disk (format inferred from extension)
avatar.save("avatar.png")
avatar.save("avatar.svg")
avatar.save("avatar.webp")

# Export formats
svg_string = avatar.to_svg()
png_bytes = avatar.to_bytes("png")
pil_image = avatar.to_image()  # PIL.Image.Image (RGBA)
data_uri = avatar.to_data_uri("svg") # "data:image/svg+xml;base64,..."
```

### Command-Line Interface (`bot-face` / `bf`)

```bash
# Generate a single avatar
bf generate "alice@example.com" --output avatar.png --radius 32
bf generate "bob@example.com" --output avatar.svg --circle

# Random generation
bf generate --random --output random_bot.png

# Output SVG to stdout (great for piping)
bf generate "charlie" --format svg > bot.svg

# Output base64 data URI for HTML/CSS
bf generate "dave" --data-uri

# Batch generate avatars for multiple users
bf batch alice bob charlie dave --output-dir ./avatars --format png --radius 24

# Inspect robot anatomy in the terminal
bf preview "octocat"

# List available color palettes
bf palettes
```

---

## 🎨 Color Palettes

| Palette | Description |
|---|---|
| `bubblegum` | Cheerful candy pinks, electric cyan, and soft yellow |
| `cyber_mint` | Vibrant neon mint, electric cyan, and cyber magenta |
| `sunny_lemon` | Bright sunshine yellow, warm coral, and sky cyan |
| `electric_berry` | Vivid magenta, electric violet, and bright lime |
| `neon_coral` | Bright warm coral, sunny gold, and cool teal |
| `aqua_splash` | Deep ocean teal, electric turquoise, and lemon pop |
| `lavender_sky` | Pastel periwinkle, lavender, and peach cream |
| `emerald_bot` | Electric lime, vivid emerald, and sunset orange |
| `arcade_pop` | 80s arcade neon pink, laser blue, and dark obsidian |
| `cotton_candy` | Soft pastel sky blue, strawberry milk, and golden vanilla |
| `sunset_glow` | Radiant tangerine, hot coral, and midnight navy |
| `matcha_latte` | Calm matcha green, creamy pistachio, and warm peach |

---

## 🛠️ Development

```bash
# Install dependencies
uv sync --extra dev

# Run full CI verification gate (lint + format-check + typecheck + test)
just verify

# Auto-format code
just format

# Run tests
just test
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
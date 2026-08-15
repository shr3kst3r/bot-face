---
id: 2026-08-14-native-svg-engine-with-pillow-rasterization
status: Accepted
supersedes: null
superseded-by: null
components: [avatar-engine, rendering, export]
ticket: null
date: 2026-08-14
---
# Use native vector SVG generation as the primary avatar engine with Pillow raster fallback

## Context

`bot-face` is a small library and CLI for generating bright, cute robot avatars for account profiles. Avatars must support variable display sizes, corner clipping (sharp, rounded rectangles with custom radii, full circle), and deterministic rendering from seeds.

Avatar generation tools face a tradeoff between vector vs. raster representations and external dependencies:
1. Pure raster generation (e.g. drawing raw pixels with Pillow or OpenCV) loses sharpness when scaled up or displayed in vector contexts (web UIs, retina screens).
2. Heavy vector-to-raster renderers (e.g. `cairosvg`, `pycairo`, `weasyprint`) require system C libraries (Cairo, Pango, GDK-Pixbuf) that are brittle to install across diverse OS environments and CI/CD pipelines.
3. Native vector SVG construction produces crisp, infinitely-scalable, zero-dependency XML markup natively compatible with web applications and modern UIs.

## Decision

We implement avatar generation as a native Python vector SVG construction engine as the canonical representation, and use Pillow (`PIL.ImageDraw`) for direct raster export to PNG/WebP without requiring system C dependencies.

The core pipeline evaluates seeded robot anatomy parameters and emits structured SVG elements. For PNG/raster requests, the avatar components are rendered directly onto a high-resolution Pillow canvas with anti-aliasing and corner clipping, or saved via Pillow.

## Consequences

### What becomes easier
- **Zero system C dependencies**: The library installs cleanly anywhere with `pip` or `uv` without requiring external Cairo/libxml2 binaries.
- **Web-native avatars**: Direct SVG output is lightweight (< 4KB), resolution-independent, and easily embedded in inline HTML or `data:image/svg+xml;base64` URIs.
- **Parametric vector design**: Geometry like rounded corners (`<rect rx="..." ry="...">`), clip paths, gradient fills, and decorative badges are naturally represented in vector notation.

### What becomes harder / accepted costs
- Maintaining parallel visual representations (SVG element tree vs. direct Pillow raster shapes) requires ensuring visual parity between SVG and PNG exports.
- Complex vector effects like complex SVG drop-shadow filters are simplified or kept to flat vector layers to ensure identical rendering across different SVG renderers and Pillow canvas.

## Alternatives considered

- **Pillow-only raster generation**: Generate only PNGs using Pillow drawing primitives. Rejected because raster-only images lose crispness on vector/retina targets and cannot be embedded cleanly as SVGs in modern web apps.
- **CairoSVG / PyCairo for SVG->PNG rasterization**: Use Cairo to convert generated SVG to PNG. Rejected because Cairo requires system-level C libraries (`libcairo`, `libpango`) that complicate cross-platform installation and break simple `uv add bot-face` workflows.

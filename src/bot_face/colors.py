"""Color palettes and color utility functions for cute robot avatar generation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    """A curated bright color palette for a cute robot avatar."""

    name: str
    description: str = ""
    background: str = Field(description="Main background color (hex)")
    background_alt: str = Field(description="Secondary background gradient color (hex)")
    chassis: str = Field(description="Main body and head color (hex)")
    chassis_dark: str = Field(description="Darker chassis shade for joints and shadow (hex)")
    chassis_outline: str = Field(
        default="#1E1E2F",
        description="High-contrast silhouette outline color (hex)",
    )
    faceplate: str = Field(description="Screen / faceplate background color (hex)")
    accent: str = Field(description="Accent color for ears, badges, antenna bulbs (hex)")
    eye_primary: str = Field(description="Primary eye color (hex)")
    eye_glow: str = Field(description="Specular eye shine or pupil color (hex)")
    mouth: str = Field(description="Mouth color (hex)")
    cheek: str = Field(description="Rosy blush cheek color (hex)")
    detail: str = Field(description="Bolts, lines, and hardware details (hex)")


PALETTES: dict[str, ColorPalette] = {
    "bubblegum": ColorPalette(
        name="bubblegum",
        description="Cheerful candy pinks, electric cyan, and soft yellow",
        background="#FFD6E8",
        background_alt="#FFB3D9",
        chassis="#FF6B9D",
        chassis_dark="#E04A7B",
        chassis_outline="#2B1020",
        faceplate="#FFFFFF",
        accent="#FFE66D",
        eye_primary="#4ECDC4",
        eye_glow="#FFFFFF",
        mouth="#E04A7B",
        cheek="#FF85A2",
        detail="#2B1020",
    ),
    "cyber_mint": ColorPalette(
        name="cyber_mint",
        description="Vibrant neon mint, electric cyan, and cyber magenta",
        background="#B8F2E6",
        background_alt="#84E6D2",
        chassis="#2EC4B6",
        chassis_dark="#1E9B8F",
        chassis_outline="#0A1E24",
        faceplate="#1A2238",
        accent="#FF3366",
        eye_primary="#48CAE4",
        eye_glow="#FFFFFF",
        mouth="#FF3366",
        cheek="#FF70A6",
        detail="#0A1E24",
    ),
    "sunny_lemon": ColorPalette(
        name="sunny_lemon",
        description="Bright sunshine yellow, warm coral, and sky cyan",
        background="#FFF3B0",
        background_alt="#FFE885",
        chassis="#FFD166",
        chassis_dark="#F4A261",
        chassis_outline="#2B1D0C",
        faceplate="#264653",
        accent="#EF476F",
        eye_primary="#06D6A0",
        eye_glow="#FFFFFF",
        mouth="#FFD166",
        cheek="#F78C6B",
        detail="#2B1D0C",
    ),
    "electric_berry": ColorPalette(
        name="electric_berry",
        description="Vivid magenta, electric violet, and bright lime",
        background="#F0E6FF",
        background_alt="#DBC4F0",
        chassis="#9B5DE5",
        chassis_dark="#7837C7",
        chassis_outline="#190730",
        faceplate="#1D1135",
        accent="#00F5D4",
        eye_primary="#F15BB5",
        eye_glow="#FFFFFF",
        mouth="#00F5D4",
        cheek="#F15BB5",
        detail="#190730",
    ),
    "neon_coral": ColorPalette(
        name="neon_coral",
        description="Bright warm coral, sunny gold, and cool teal",
        background="#FFE5D9",
        background_alt="#FFCAD4",
        chassis="#FF6F59",
        chassis_dark="#DB4C37",
        chassis_outline="#26100D",
        faceplate="#254441",
        accent="#43BCCD",
        eye_primary="#F6C85F",
        eye_glow="#FFFFFF",
        mouth="#43BCCD",
        cheek="#FF8E72",
        detail="#26100D",
    ),
    "aqua_splash": ColorPalette(
        name="aqua_splash",
        description="Deep ocean teal, electric turquoise, and lemon pop",
        background="#D0F4DE",
        background_alt="#A9DFBF",
        chassis="#00BBF9",
        chassis_dark="#0096C7",
        chassis_outline="#0A1D33",
        faceplate="#FFFFFF",
        accent="#FEE440",
        eye_primary="#00F5D4",
        eye_glow="#FFFFFF",
        mouth="#0096C7",
        cheek="#FF99C8",
        detail="#0A1D33",
    ),
    "lavender_sky": ColorPalette(
        name="lavender_sky",
        description="Pastel periwinkle, lavender, and peach cream",
        background="#E8EAFF",
        background_alt="#D0D5FF",
        chassis="#8338EC",
        chassis_dark="#6218CC",
        chassis_outline="#1C0D38",
        faceplate="#FFFFFF",
        accent="#FFBE0B",
        eye_primary="#3A86FF",
        eye_glow="#FFFFFF",
        mouth="#FB5607",
        cheek="#FF85A2",
        detail="#1C0D38",
    ),
    "emerald_bot": ColorPalette(
        name="emerald_bot",
        description="Electric lime, vivid emerald, and sunset orange",
        background="#E8F8F5",
        background_alt="#C8F2E7",
        chassis="#10B981",
        chassis_dark="#059669",
        chassis_outline="#06261C",
        faceplate="#0F172A",
        accent="#F59E0B",
        eye_primary="#38BDF8",
        eye_glow="#FFFFFF",
        mouth="#10B981",
        cheek="#F472B6",
        detail="#06261C",
    ),
    "arcade_pop": ColorPalette(
        name="arcade_pop",
        description="80s arcade neon pink, laser blue, and dark obsidian",
        background="#FCE7F3",
        background_alt="#FBCFE8",
        chassis="#EC4899",
        chassis_dark="#BE185D",
        chassis_outline="#1F0514",
        faceplate="#090A0F",
        accent="#06B6D4",
        eye_primary="#FACC15",
        eye_glow="#FFFFFF",
        mouth="#06B6D4",
        cheek="#F43F5E",
        detail="#1F0514",
    ),
    "cotton_candy": ColorPalette(
        name="cotton_candy",
        description="Soft pastel sky blue, strawberry milk, and golden vanilla",
        background="#E0F2FE",
        background_alt="#BAE6FD",
        chassis="#38BDF8",
        chassis_dark="#0284C7",
        chassis_outline="#0C2333",
        faceplate="#FFFFFF",
        accent="#F472B6",
        eye_primary="#6366F1",
        eye_glow="#FFFFFF",
        mouth="#0284C7",
        cheek="#FDA4AF",
        detail="#0C2333",
    ),
    "sunset_glow": ColorPalette(
        name="sunset_glow",
        description="Radiant tangerine, hot coral, and midnight navy",
        background="#FEF3C7",
        background_alt="#FDE68A",
        chassis="#FB923C",
        chassis_dark="#EA580C",
        chassis_outline="#2B1305",
        faceplate="#1E1B4B",
        accent="#A855F7",
        eye_primary="#38BDF8",
        eye_glow="#FFFFFF",
        mouth="#FDE047",
        cheek="#F43F5E",
        detail="#2B1305",
    ),
    "matcha_latte": ColorPalette(
        name="matcha_latte",
        description="Calm matcha green, creamy pistachio, and warm peach",
        background="#F0FDF4",
        background_alt="#DCFCE7",
        chassis="#84CC16",
        chassis_dark="#65A30D",
        chassis_outline="#162905",
        faceplate="#14532D",
        accent="#F97316",
        eye_primary="#FEF08A",
        eye_glow="#FFFFFF",
        mouth="#84CC16",
        cheek="#FB7185",
        detail="#162905",
    ),
    "vaporwave": ColorPalette(
        name="vaporwave",
        description="Pastel neon pink, cyan blue, and twilight purple",
        background="#F5D0FE",
        background_alt="#E879F9",
        chassis="#C084FC",
        chassis_dark="#9333EA",
        chassis_outline="#210838",
        faceplate="#2E1065",
        accent="#22D3EE",
        eye_primary="#F43F5E",
        eye_glow="#FFFFFF",
        mouth="#22D3EE",
        cheek="#F472B6",
        detail="#210838",
    ),
    "solar_flare": ColorPalette(
        name="solar_flare",
        description="Blazing crimson red, solar yellow, and fiery orange",
        background="#FEE2E2",
        background_alt="#FECACA",
        chassis="#EF4444",
        chassis_dark="#DC2626",
        chassis_outline="#3B0808",
        faceplate="#450A0A",
        accent="#FACC15",
        eye_primary="#38BDF8",
        eye_glow="#FFFFFF",
        mouth="#FDE047",
        cheek="#FB923C",
        detail="#3B0808",
    ),
    "tokyo_night": ColorPalette(
        name="tokyo_night",
        description="Electric cyan, neon violet, and night obsidian",
        background="#E0E7FF",
        background_alt="#C7D2FE",
        chassis="#6366F1",
        chassis_dark="#4338CA",
        chassis_outline="#101033",
        faceplate="#0B0F19",
        accent="#F43F5E",
        eye_primary="#06B6D4",
        eye_glow="#FFFFFF",
        mouth="#F43F5E",
        cheek="#FB7185",
        detail="#101033",
    ),
    "bumblebee": ColorPalette(
        name="bumblebee",
        description="Bright bumblebee yellow, jet black, and warm amber",
        background="#FEF9C3",
        background_alt="#FEF08A",
        chassis="#EAB308",
        chassis_dark="#CA8A04",
        chassis_outline="#1C1502",
        faceplate="#18181B",
        accent="#F97316",
        eye_primary="#38BDF8",
        eye_glow="#FFFFFF",
        mouth="#EAB308",
        cheek="#FB923C",
        detail="#1C1502",
    ),
    "aurora_borealis": ColorPalette(
        name="aurora_borealis",
        description="Shimmering emerald, polar cyan, and celestial violet",
        background="#CCFBF1",
        background_alt="#99F6E4",
        chassis="#14B8A6",
        chassis_dark="#0D9488",
        chassis_outline="#052420",
        faceplate="#042F2E",
        accent="#A855F7",
        eye_primary="#67E8F9",
        eye_glow="#FFFFFF",
        mouth="#67E8F9",
        cheek="#F472B6",
        detail="#052420",
    ),
    "cherry_blossom": ColorPalette(
        name="cherry_blossom",
        description="Soft sakura pink, rose crimson, and ivory cream",
        background="#FFF1F2",
        background_alt="#FFE4E6",
        chassis="#FB7185",
        chassis_dark="#E11D48",
        chassis_outline="#330914",
        faceplate="#4C0519",
        accent="#FBBF24",
        eye_primary="#34D399",
        eye_glow="#FFFFFF",
        mouth="#FBBF24",
        cheek="#FDA4AF",
        detail="#330914",
    ),
    "poison_ivy": ColorPalette(
        name="poison_ivy",
        description="Neon slime green, toxic lime, and electric violet",
        background="#ECFCCB",
        background_alt="#D9F99D",
        chassis="#65A30D",
        chassis_dark="#4D7C0F",
        chassis_outline="#1A2E05",
        faceplate="#1A2E05",
        accent="#C084FC",
        eye_primary="#A3E635",
        eye_glow="#FFFFFF",
        mouth="#C084FC",
        cheek="#F472B6",
        detail="#1A2E05",
    ),
    "glacier_ice": ColorPalette(
        name="glacier_ice",
        description="Ice crystal cyan, frost blue, and arctic snow",
        background="#CFFAFE",
        background_alt="#A5F3FC",
        chassis="#06B6D4",
        chassis_dark="#0891B2",
        chassis_outline="#06222B",
        faceplate="#083344",
        accent="#F59E0B",
        eye_primary="#67E8F9",
        eye_glow="#FFFFFF",
        mouth="#67E8F9",
        cheek="#F472B6",
        detail="#06222B",
    ),
    "papaya_punch": ColorPalette(
        name="papaya_punch",
        description="Tropical papaya orange, guava pink, and palm green",
        background="#FFEDD5",
        background_alt="#FED7AA",
        chassis="#F97316",
        chassis_dark="#EA580C",
        chassis_outline="#331405",
        faceplate="#431407",
        accent="#10B981",
        eye_primary="#FDE047",
        eye_glow="#FFFFFF",
        mouth="#10B981",
        cheek="#FB7185",
        detail="#331405",
    ),
}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string (e.g. '#FF6B9D' or 'FF6B9D') to an (R, G, B) tuple."""
    clean_hex = hex_color.lstrip("#")
    if len(clean_hex) == 3:
        clean_hex = "".join(c * 2 for c in clean_hex)
    if len(clean_hex) != 6:
        msg = f"Invalid hex color: '{hex_color}'"
        raise ValueError(msg)
    r = int(clean_hex[0:2], 16)
    g = int(clean_hex[2:4], 16)
    b = int(clean_hex[4:6], 16)
    return (r, g, b)


def hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    """Convert a hex color string to an (R, G, B, A) tuple."""
    r, g, b = hex_to_rgb(hex_color)
    return (r, g, b, alpha)


def get_palette(name: str) -> ColorPalette:
    """Retrieve a palette by name. Raises ValueError if name is unknown."""
    normalized = name.lower().replace("-", "_").strip()
    if normalized not in PALETTES:
        available = ", ".join(sorted(PALETTES.keys()))
        msg = f"Unknown palette '{name}'. Available palettes: {available}"
        raise ValueError(msg)
    return PALETTES[normalized]


def list_palettes() -> list[str]:
    """Return a sorted list of all available palette names."""
    return sorted(PALETTES.keys())

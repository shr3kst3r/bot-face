"""Deterministic generator that samples avatar anatomy from seeds."""

from __future__ import annotations

import hashlib
import random
import secrets
from typing import Any

from bot_face.colors import get_palette, list_palettes
from bot_face.config import AvatarConfig
from bot_face.models import RobotAnatomy, RobotAvatar

HEAD_STYLES = [
    "tv_monitor",
    "rounded_capsule",
    "retro_dome",
    "rounded_box",
    "curved_hexagon",
    "cat_ears",
    "bear_ears",
    "bunny_ears",
    "astronaut_helmet",
]

FACEPLATE_STYLES = ["screen", "inset", "bezel", "glowing", "flat"]

EYEWEAR_STYLES = ["glasses", "sunglasses", "retro_goggles", "cyclops_visor"]
NON_EYEWEAR_STYLES = [
    "glossy_pupil",
    "sparkle_anime",
    "feline_slits",
    "wink",
    "spiral",
    "led_matrix_happy",
    "led_matrix_dots",
    "led_matrix_stars",
    "led_matrix_hearts",
]
ALL_EYE_STYLES = NON_EYEWEAR_STYLES + EYEWEAR_STYLES

MOUTH_STYLES = [
    "happy_smile",
    "open_smile",
    "cat_mouth",
    "vamp_fang",
    "mustache_grill",
    "speaker_grill",
    "wave_oscilloscope",
    "toothy_grin",
    "led_meter",
    "cute_o",
]

ANTENNA_STYLES = [
    "single_ball",
    "dual_springs",
    "radar_dish",
    "lightning",
    "beacon_light",
    "earmuffs",
    "side_screws",
    "halo",
    "flower",
    "devil_horns",
    "lightbulb",
    "none",
]

TORSO_STYLES = ["curved_chest", "striped_neck", "riveted_collar", "coil_connector", "bell_collar"]

BADGE_STYLES = [
    "heart",
    "star",
    "battery_meter",
    "power_button",
    "bolt",
    "bowtie",
    "shield",
    "reactor",
    "pawprint",
    "fishbone",
]
ALL_BADGE_STYLES = [
    "none",
    "none",
    "heart",
    "star",
    "battery_meter",
    "power_button",
    "bolt",
    "bowtie",
    "shield",
    "reactor",
    "pawprint",
    "fishbone",
]

HAT_STYLES = ["party_hat", "bowler_hat", "propeller_cap", "beanie", "crown", "chef_hat"]
ALL_HAT_STYLES = [
    "none",
    "none",
    "party_hat",
    "bowler_hat",
    "propeller_cap",
    "beanie",
    "crown",
    "chef_hat",
]

CHEEK_STYLES = ["round_blush", "round_blush", "dash_blush", "heart_blush", "freckles", "none"]
BACKGROUND_STYLES = ["solid", "linear_gradient", "radial_gradient"]
EAR_DETAILS = ["bolts", "rings", "vents", "plain"]
FOREHEAD_DETAILS = ["none", "rivets", "gem", "antennae_mount", "stripe"]


def seed_to_int(seed: Any) -> int:
    """Convert any seed type (str, int, bytes, None) into a deterministic 64-bit integer."""
    if seed is None:
        return secrets.randbits(63)
    if isinstance(seed, int):
        return abs(seed) % (2**63 - 1)
    raw_bytes = seed if isinstance(seed, bytes) else str(seed).encode("utf-8")

    digest = hashlib.sha256(raw_bytes).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=False)


def generate(
    seed: Any = None,
    size: int = 256,
    corner_radius: int = 0,
    circle: bool = False,
    palette: str | None = None,
    filter: str | None = None,
    has_hat: bool | None = None,
    has_glasses: bool | None = None,
    has_badge: bool | None = None,
    cat: bool | None = None,
) -> RobotAvatar:
    """Generate a cute robot avatar from configuration options and seed."""
    effective_seed = seed
    seed_int = seed_to_int(effective_seed)
    rng = random.Random(seed_int)

    # Palette selection
    if palette is not None:
        color_palette = get_palette(palette)
    else:
        palette_names = list_palettes()
        chosen_palette = rng.choice(palette_names)
        color_palette = get_palette(chosen_palette)

    # Cat feature overrides
    if cat is True:
        head_style = "cat_ears"
        mouth_style = rng.choice(["cat_mouth", "happy_smile", "open_smile", "vamp_fang"])
        has_whiskers = True
    elif cat is False:
        non_cat_heads = [h for h in HEAD_STYLES if h != "cat_ears"]
        head_style = rng.choice(non_cat_heads)
        mouth_style = rng.choice(MOUTH_STYLES)
        has_whiskers = False
    else:
        head_style = rng.choice(HEAD_STYLES)
        mouth_style = rng.choice(MOUTH_STYLES)
        has_whiskers = (head_style == "cat_ears" and rng.random() < 0.8) or (rng.random() < 0.15)

    faceplate_style = rng.choice(FACEPLATE_STYLES)

    # Sample eyes & glasses
    if has_glasses is True:
        eye_style = rng.choice(EYEWEAR_STYLES)
    elif has_glasses is False:
        eye_style = rng.choice(NON_EYEWEAR_STYLES)
    else:
        if cat is True:
            eye_style = rng.choice(
                [
                    "feline_slits",
                    "glossy_pupil",
                    "sparkle_anime",
                    "wink",
                    "led_matrix_happy",
                    "sunglasses",
                ]
            )
        else:
            eye_style = rng.choice(ALL_EYE_STYLES)

    # Sample antennae (if head has animal ears, soften antenna probability)
    if head_style in ("cat_ears", "bear_ears", "bunny_ears"):
        antenna_style = rng.choice(
            ["none", "none", "single_ball", "beacon_light", "halo", "flower"]
        )
    else:
        antenna_style = rng.choice(ANTENNA_STYLES)

    # Sample torso & badge
    if cat is True:
        torso_style = rng.choice(["bell_collar", "bell_collar", "curved_chest", "striped_neck"])
    else:
        torso_style = rng.choice(TORSO_STYLES)

    if has_badge is True:
        if cat is True:
            badge_style = rng.choice(["pawprint", "fishbone", "heart", "bell"])
        else:
            badge_style = rng.choice(BADGE_STYLES)
    elif has_badge is False:
        badge_style = "none"
    else:
        if cat is True:
            badge_style = rng.choice(["pawprint", "fishbone", "heart", "none", "none"])
        else:
            badge_style = rng.choice(ALL_BADGE_STYLES)

    # Sample hat
    if has_hat is True:
        hat_style = rng.choice(HAT_STYLES)
    elif has_hat is False:
        hat_style = "none"
    else:
        if head_style in ("cat_ears", "bear_ears", "bunny_ears"):
            hat_style = rng.choice(["none", "none", "none", "party_hat", "crown", "chef_hat"])
        else:
            hat_style = rng.choice(ALL_HAT_STYLES)

    # If wearing a bulky hat, avoid tall center antenna conflict
    if hat_style in ("bowler_hat", "beanie", "crown", "chef_hat") and antenna_style not in (
        "earmuffs",
        "side_screws",
    ):
        antenna_style = "none"

    cheek_style = rng.choice(CHEEK_STYLES)
    background_style = rng.choice(BACKGROUND_STYLES)
    ear_detail = rng.choice(EAR_DETAILS)
    forehead_detail = rng.choice(FOREHEAD_DETAILS)

    anatomy = RobotAnatomy(
        head_style=head_style,
        faceplate_style=faceplate_style,
        eye_style=eye_style,
        mouth_style=mouth_style,
        antenna_style=antenna_style,
        torso_style=torso_style,
        badge_style=badge_style,
        hat_style=hat_style,
        cheek_style=cheek_style,
        background_style=background_style,
        ear_detail=ear_detail,
        forehead_detail=forehead_detail,
        has_whiskers=has_whiskers,
    )

    config = AvatarConfig(
        seed=effective_seed,
        size=size,
        corner_radius=corner_radius,
        circle=circle,
        palette=palette,
        filter=filter,
        has_hat=has_hat,
        has_glasses=has_glasses,
        has_badge=has_badge,
        cat=cat,
    )

    return RobotAvatar(
        seed=effective_seed if effective_seed is not None else seed_int,
        config=config,
        palette=color_palette,
        anatomy=anatomy,
        viewbox_size=256,
    )

"""Tests for the deterministic generator."""

from __future__ import annotations

from bot_face.generator import generate, seed_to_int


def test_seed_to_int_determinism() -> None:
    s1 = seed_to_int("alice@example.com")
    s2 = seed_to_int("alice@example.com")
    assert s1 == s2
    assert isinstance(s1, int)

    # Bytes and int
    assert seed_to_int(12345) == 12345
    assert seed_to_int(b"alice@example.com") == s1

    # Random seed when None
    r1 = seed_to_int(None)
    r2 = seed_to_int(None)
    assert isinstance(r1, int)
    assert isinstance(r2, int)


def test_generate_determinism() -> None:
    bot1 = generate(seed="hero_bot", size=256, corner_radius=16)
    bot2 = generate(seed="hero_bot", size=256, corner_radius=16)

    assert bot1.palette.name == bot2.palette.name
    assert bot1.anatomy == bot2.anatomy
    assert bot1.to_svg() == bot2.to_svg()
    assert bot1.to_bytes("png") == bot2.to_bytes("png")


def test_generate_different_seeds_differ() -> None:
    bot_a = generate(seed="alpha")
    bot_b = generate(seed="beta")

    # The anatomies or palettes should differ
    assert (bot_a.anatomy != bot_b.anatomy) or (bot_a.palette.name != bot_b.palette.name)


def test_generate_explicit_palette() -> None:
    bot = generate(seed="test", palette="sunny_lemon")
    assert bot.palette.name == "sunny_lemon"


def test_generate_hat_override() -> None:
    bot_with_hat = generate(seed="test", has_hat=True)
    assert bot_with_hat.anatomy.hat_style != "none"

    bot_no_hat = generate(seed="test", has_hat=False)
    assert bot_no_hat.anatomy.hat_style == "none"


def test_generate_glasses_override() -> None:
    bot_with_glasses = generate(seed="test", has_glasses=True)
    assert bot_with_glasses.anatomy.eye_style in [
        "glasses",
        "sunglasses",
        "retro_goggles",
        "cyclops_visor",
    ]

    bot_no_glasses = generate(seed="test", has_glasses=False)
    assert bot_no_glasses.anatomy.eye_style not in [
        "glasses",
        "sunglasses",
        "retro_goggles",
        "cyclops_visor",
    ]


def test_generate_badge_override() -> None:
    bot_with_badge = generate(seed="test", has_badge=True)
    assert bot_with_badge.anatomy.badge_style in [
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

    bot_no_badge = generate(seed="test", has_badge=False)
    assert bot_no_badge.anatomy.badge_style == "none"


def test_generate_cat_override() -> None:
    cat_bot = generate(seed="cat_test", cat=True)
    assert cat_bot.anatomy.head_style == "cat_ears"
    assert cat_bot.anatomy.has_whiskers is True
    assert cat_bot.to_svg().startswith("<svg")

    non_cat_bot = generate(seed="cat_test", cat=False)
    assert non_cat_bot.anatomy.head_style != "cat_ears"
    assert non_cat_bot.anatomy.has_whiskers is False


def test_generate_shading_override() -> None:
    shaded = generate(seed="shading_test", shading=True)
    assert shaded.config.shading is True
    assert "chassis-grad" in shaded.to_svg()
    assert shaded.to_image().size == (256, 256)

    flat = generate(seed="shading_test", shading=False)
    assert flat.config.shading is False
    assert flat.to_svg().startswith("<svg")
    assert flat.to_image().size == (256, 256)


def test_generate_mood_presets() -> None:
    love_bot = generate(seed="mood_love", mood="love")
    assert love_bot.anatomy.eye_style == "led_matrix_hearts"
    assert love_bot.anatomy.cheek_style == "heart_blush"
    assert love_bot.anatomy.badge_style == "heart"

    surprised_bot = generate(seed="mood_surprised", mood="surprised")
    assert surprised_bot.anatomy.mouth_style == "cute_o"

    wink_bot = generate(seed="mood_wink", mood="wink")
    assert wink_bot.anatomy.eye_style == "wink"


def test_generate_animal_presets() -> None:
    bunny_bot = generate(seed="bunny_123", animal="bunny")
    assert bunny_bot.anatomy.head_style == "bunny_ears"
    assert bunny_bot.anatomy.has_whiskers is True

    bear_bot = generate(seed="bear_123", animal="bear")
    assert bear_bot.anatomy.head_style == "bear_ears"


def test_generate_transparent_and_bg_override() -> None:
    transparent_bot = generate(seed="trans_bot", transparent=True)
    assert transparent_bot.config.transparent is True
    svg = transparent_bot.to_svg()
    # In transparent mode, no background rect fill is drawn
    assert '<rect x="0" y="0" width="256" height="256" fill=' not in svg

    custom_bg_bot = generate(seed="custom_bg", background_color="#123456")
    assert custom_bg_bot.config.background_color == "#123456"
    assert "#123456" in custom_bg_bot.to_svg()

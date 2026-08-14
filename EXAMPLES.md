# 🤖 Bot-Face Examples & Gallery

A collection of example robot avatars generated with `bot-face`, demonstrating bright color palettes, sharp high-contrast outlines that pop off any background, expressive robot anatomy, and retro visual filters.

---

## 🎨 Gallery

| Preview | Seed | Palette | Filter / Style | Description |
|---|---|---|---|---|
| <img src="docs/examples/alice_at_example_com.png" width="128" /> | `alice@example.com` | `bubblegum` | None (Radius: 32px) | Sweet Bubblegum robot with sparkling kawaii eyes, blushing cheeks, rounded corners, and crisp dark outlines. |
| <img src="docs/examples/cyber_samurai.png" width="128" /> | `cyber_samurai` | `cyber_mint` | `8bit` (Radius: 16px) | Chunky 8-bit retro arcade pixel art in vibrant neon mint and cyan with bold pixel silhouette. |
| <img src="docs/examples/arcade_champion.png" width="128" /> | `arcade_champion` | `arcade_pop` | `16bit` (Radius: 24px) | 16-bit SNES/Genesis pixel art style with Floyd-Steinberg dither and cool shades. |
| <img src="docs/examples/gameboy_nostalgia.png" width="128" /> | `gameboy_nostalgia` | `cyber_mint` | `gameboy` | Classic 4-shade olive green Nintendo Game Boy DMG-01 LCD screen. |
| <img src="docs/examples/sunny_explorer.png" width="128" /> | `sunny_explorer` | `sunny_lemon` | Circle Clip | Cheerful yellow circular profile avatar with spinning propeller beanie cap. |
| <img src="docs/examples/electric_monarch.png" width="128" /> | `electric_monarch` | `electric_berry` | None (Radius: 32px) | Royal electric violet robot with glowing star eyes and golden jewel crown. |
| <img src="docs/examples/neon_drifter.png" width="128" /> | `neon_drifter` | `neon_coral` | `crt` (Radius: 20px) | Retro arcade CRT television monitor filter with scanlines and phosphor bloom. |
| <img src="docs/examples/aqua_diver.png" width="128" /> | `aqua_diver` | `aqua_splash` | Circle Clip | Deep ocean teal circular avatar with chunky headphone earmuffs and cat smile (`:3`). |
| <img src="docs/examples/cosmic_party.png" width="128" /> | `cosmic_party` | `lavender_sky` | None (Radius: 28px) | Festive lavender robot with party cone hat, bowtie, and happy LED matrix (`^ ^`) eyes. |
| <img src="docs/examples/emerald_guardian.png" width="128" /> | `emerald_guardian` | `emerald_bot` | None (Radius: 24px) | Emerald green bot with gentleman bowler hat, mustache grill, and battery power meter. |
| <img src="docs/examples/cotton_sweetie.png" width="128" /> | `cotton_sweetie` | `cotton_candy` | None (Radius: 36px) | Pastel strawberry milk bot with robotic cat ears, rosy cheeks, and playful wink. |
| <img src="docs/examples/sunset_rider.png" width="128" /> | `sunset_glow` | `sunset_glow` | None (Radius: 16px) | Radiant sunset orange robot with lightning bolt antenna, sunglasses, and shield badge. |
| <img src="docs/examples/matcha_latte_bot.png" width="128" /> | `matcha_latte_bot` | `matcha_latte` | None (Radius: 32px) | Calming matcha green robot with glowing heart LED eyes (`♥ ♥`) and sprout flower. |
| <img src="docs/examples/angelic_bot.png" width="128" /> | `angelic_bot` | `aurora_borealis` | None (Radius: 28px) | Celestial aurora bot with a floating glowing angel halo and arc reactor core. |
| <img src="docs/examples/bunny_chef.png" width="128" /> | `bunny_chef` | `cherry_blossom` | None (Radius: 32px) | Sakura pink robot with tall robotic bunny ears, chef hat, and cute vamp fangs. |
| <img src="docs/examples/bumblebee_racer.png" width="128" /> | `bumblebee_racer` | `bumblebee` | None (Radius: 20px) | High-contrast bumblebee yellow racer robot with cyclops visor. |
| <img src="docs/examples/blueprint_mech.png" width="128" /> | `blueprint_mech` | `tokyo_night` | `blueprint` (Radius: 16px) | Architectural cyan & navy technical blueprint line art schematic. |
| <img src="docs/examples/vintage_sepia.png" width="128" /> | `vintage_sepia` | `solar_flare` | `sepia` (Radius: 24px) | Warm nostalgic vintage sepia photograph robot portrait. |
| <img src="docs/examples/dither_matrix.png" width="128" /> | `dither_matrix` | `vaporwave` | `dither` | Floyd-Steinberg 1-bit dot matrix dithered newspaper/terminal style. |
| <img src="docs/examples/neon_cyber_bloom.png" width="128" /> | `neon_cyber_bloom` | `poison_ivy` | `neon_glow` (Radius: 32px) | Intense cyberpunk neon bloom with saturated toxic glow. |

---

## 💻 How to Reproduce Each Example

### 1. Classic Account Avatar (`alice@example.com`)
```bash
bf generate "alice@example.com" --palette bubblegum --radius 32 --output alice.png
```
```python
import bot_face

avatar = bot_face.generate(seed="alice@example.com", palette="bubblegum", corner_radius=32)
avatar.save("alice.png")
```

### 2. 8-Bit Pixel Art (`cyber_samurai`)
```bash
bf generate "cyber_samurai" --palette cyber_mint --filter 8bit --radius 16 --output samurai.png
```

### 3. 16-Bit Arcade Hero (`arcade_champion`)
```bash
bf generate "arcade_champion" --palette arcade_pop --filter 16bit --radius 24 --output arcade.png
```

### 4. Game Boy DMG-01 (`gameboy_nostalgia`)
```bash
bf generate "gameboy_nostalgia" --filter gameboy --output gameboy.png
```

### 5. Angelic Halo Robot (`angelic_bot`)
```bash
bf generate "angelic_bot" --palette aurora_borealis --radius 28 --output angel.png
```

### 6. Bunny Chef Robot (`bunny_chef`)
```bash
bf generate "bunny_chef" --palette cherry_blossom --radius 32 --output chef.png
```

### 7. Circular Avatar with Propeller Beanie (`sunny_explorer`)
```bash
bf generate "sunny_explorer" --palette sunny_lemon --circle --output sunny.png
```

### 8. CRT Television Screen (`neon_drifter`)
```bash
bf generate "neon_drifter" --palette neon_coral --filter crt --radius 20 --output crt.png
```

### 9. Blueprint Schematic (`blueprint_mech`)
```bash
bf generate "blueprint_mech" --filter blueprint --radius 16 --output blueprint.png
```

### 10. Neon Cyber Bloom (`neon_cyber_bloom`)
```bash
bf generate "neon_cyber_bloom" --palette poison_ivy --filter neon_glow --radius 32 --output neon.png
```

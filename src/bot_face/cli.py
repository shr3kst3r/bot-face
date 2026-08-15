"""Command Line Interface for bot-face avatar generator."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bot_face.colors import PALETTES, get_palette, list_palettes
from bot_face.filters import AVAILABLE_FILTERS, list_filters
from bot_face.generator import MOOD_PRESETS, generate

app = typer.Typer(
    name="bot-face",
    help="🤖 Cute robot avatar generator library and CLI for account profile images.",
    no_args_is_help=True,
    add_completion=True,
)

console = Console()
err_console = Console(stderr=True)


def version_callback(value: bool) -> None:
    if value:
        import bot_face

        console.print(f"bot-face v{bot_face.__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Show the application version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """Cute robot avatar generator."""


@app.command(name="generate", help="Generate a single robot avatar.")
def generate_cmd(
    seed: Annotated[
        str | None,
        typer.Argument(
            help="Seed string (username, email, id) to deterministically generate features. "
            "If omitted, a random seed is chosen.",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output filepath. Extension determines format (.png, .svg, .webp).",
        ),
    ] = None,
    format_opt: Annotated[
        str | None,
        typer.Option(
            "--format",
            "-f",
            help="Explicit format ('png', 'svg', 'webp', 'jpg').",
        ),
    ] = None,
    size: Annotated[
        int,
        typer.Option(
            "--size",
            "-s",
            help="Output image size (width and height) in pixels.",
            min=16,
            max=4096,
        ),
    ] = 256,
    radius: Annotated[
        int,
        typer.Option(
            "--radius",
            "-r",
            help="Corner radius in pixels (0 for square, >0 for rounded rectangle).",
            min=0,
        ),
    ] = 0,
    circle: Annotated[
        bool,
        typer.Option(
            "--circle",
            "-c",
            help="Clip the avatar into a circular shape.",
        ),
    ] = False,
    random_seed: Annotated[
        bool,
        typer.Option(
            "--random",
            help="Force a random cryptographic seed regardless of input.",
        ),
    ] = False,
    palette: Annotated[
        str | None,
        typer.Option(
            "--palette",
            "-p",
            help="Color palette name (run 'bot-face palettes' to list).",
        ),
    ] = None,
    filter_opt: Annotated[
        str | None,
        typer.Option(
            "--filter",
            "-F",
            help="Retro style or filter: '8bit', '16bit', 'gameboy', 'crt', etc.",
        ),
    ] = None,
    hat: Annotated[
        bool | None,
        typer.Option(
            "--hat/--no-hat",
            help="Force hat presence or absence.",
        ),
    ] = None,
    glasses: Annotated[
        bool | None,
        typer.Option(
            "--glasses/--no-glasses",
            help="Force glasses/eyewear presence or absence.",
        ),
    ] = None,
    badge: Annotated[
        bool | None,
        typer.Option(
            "--badge/--no-badge",
            help="Force chest badge presence or absence.",
        ),
    ] = None,
    cat: Annotated[
        bool | None,
        typer.Option(
            "--cat/--no-cat",
            help="Force cute cat robot features (cat ears, whiskers, cat mouth).",
        ),
    ] = None,
    bunny: Annotated[
        bool,
        typer.Option(
            "--bunny",
            help="Force cute bunny robot features (bunny ears, whiskers).",
        ),
    ] = False,
    bear: Annotated[
        bool,
        typer.Option(
            "--bear",
            help="Force cute bear robot features (rounded bear ears).",
        ),
    ] = False,
    animal: Annotated[
        str | None,
        typer.Option(
            "--animal",
            "-a",
            help="Animal robot preset: 'cat', 'bunny', 'bear'.",
        ),
    ] = None,
    mood: Annotated[
        str | None,
        typer.Option(
            "--mood",
            "-m",
            help="Expression preset: 'happy', 'cool', 'love', 'surprised', 'wink', etc.",
        ),
    ] = None,
    transparent: Annotated[
        bool,
        typer.Option(
            "--transparent/--no-transparent",
            help="Render with a transparent background.",
        ),
    ] = False,
    bg_color: Annotated[
        str | None,
        typer.Option(
            "--bg-color",
            "--bg",
            help="Custom background color override (hex).",
        ),
    ] = None,
    shading: Annotated[
        bool,
        typer.Option(
            "--shading/--no-shading",
            help="Enable or disable 3D cel-shading, highlights, and depth bevels.",
        ),
    ] = True,
    data_uri: Annotated[
        bool,
        typer.Option(
            "--data-uri",
            help="Output as data: URI string for HTML/CSS <img> tags.",
        ),
    ] = False,
) -> None:
    """Generate a cute robot avatar."""
    if palette:
        try:
            get_palette(palette)
        except ValueError as e:
            err_console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1) from e

    if filter_opt and filter_opt.lower() not in AVAILABLE_FILTERS:
        valid = ", ".join(list_filters())
        err_console.print(
            f"[bold red]Error:[/bold red] Unknown filter '{filter_opt}'. Available: {valid}"
        )
        raise typer.Exit(code=1)

    effective_animal = animal
    if bunny:
        effective_animal = "bunny"
    elif bear:
        effective_animal = "bear"
    elif cat is True:
        effective_animal = "cat"

    effective_seed = None if random_seed else seed
    avatar = generate(
        seed=effective_seed,
        size=size,
        corner_radius=radius,
        circle=circle,
        palette=palette,
        filter=filter_opt,
        has_hat=hat,
        has_glasses=glasses,
        has_badge=badge,
        cat=cat,
        animal=effective_animal,
        mood=mood,
        transparent=transparent,
        background_color=bg_color,
        shading=shading,
    )

    # If data-uri requested
    if data_uri:
        fmt = format_opt or (output.suffix.lstrip(".") if output else "svg")
        uri = avatar.to_data_uri(format=fmt)
        if output:
            output.write_text(uri, encoding="utf-8")
            console.print(f"[green]✓[/green] Wrote data URI to [bold]{output}[/bold]")
        else:
            console.print(uri)
        return

    # If output file provided
    if output is not None:
        saved_path = avatar.save(output, format=format_opt)
        pal_name = avatar.palette.name
        console.print(
            f"[green]✓[/green] Generated avatar -> [bold]{saved_path}[/bold] "
            f"([cyan]{pal_name}[/cyan], {size}x{size}px)"
        )
        return

    # Default: if no output file specified, write SVG to stdout
    fmt = (format_opt or "svg").lower()
    if fmt == "svg":
        sys.stdout.write(avatar.to_svg())
    else:
        # Fallback stdout for binary: base64 data URI
        sys.stdout.write(avatar.to_data_uri(format=fmt) + "\n")


@app.command(name="batch", help="Batch generate multiple avatars for a list of seeds.")
def batch_cmd(
    seeds: Annotated[
        list[str],
        typer.Argument(
            help="List of seeds (usernames, emails, ids) to generate avatars for.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory to save generated avatars.",
        ),
    ] = Path("./avatars"),
    format_opt: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="Output format: 'png', 'svg', 'webp'.",
        ),
    ] = "png",
    size: Annotated[
        int,
        typer.Option(
            "--size",
            "-s",
            help="Image size in pixels.",
            min=16,
            max=4096,
        ),
    ] = 256,
    radius: Annotated[
        int,
        typer.Option(
            "--radius",
            "-r",
            help="Corner radius in pixels.",
            min=0,
        ),
    ] = 0,
    circle: Annotated[
        bool,
        typer.Option(
            "--circle",
            "-c",
            help="Clip the avatar into a circular shape.",
        ),
    ] = False,
    palette: Annotated[
        str | None,
        typer.Option(
            "--palette",
            "-p",
            help="Color palette name (if omitted, chosen deterministically per seed).",
        ),
    ] = None,
    filter_opt: Annotated[
        str | None,
        typer.Option(
            "--filter",
            "-F",
            help="Retro style or filter: '8bit', '16bit', 'gameboy', 'crt', etc.",
        ),
    ] = None,
    cat: Annotated[
        bool | None,
        typer.Option(
            "--cat/--no-cat",
            help="Force cute cat robot features (cat ears, whiskers, cat mouth).",
        ),
    ] = None,
    animal: Annotated[
        str | None,
        typer.Option(
            "--animal",
            "-a",
            help="Animal preset: 'cat', 'bunny', 'bear'.",
        ),
    ] = None,
    mood: Annotated[
        str | None,
        typer.Option(
            "--mood",
            "-m",
            help="Expression preset: 'happy', 'cool', 'love', 'surprised', 'wink', etc.",
        ),
    ] = None,
    transparent: Annotated[
        bool,
        typer.Option(
            "--transparent/--no-transparent",
            help="Render with a transparent background.",
        ),
    ] = False,
    shading: Annotated[
        bool,
        typer.Option(
            "--shading/--no-shading",
            help="Enable or disable 3D cel-shading and highlights.",
        ),
    ] = True,
) -> None:
    """Generate multiple avatars in batch."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ext = format_opt.lower().lstrip(".")

    console.print(
        f"[bold]Generating {len(seeds)} avatar(s) to [cyan]{output_dir}/[/cyan] "
        f"({ext.upper()})...[/bold]"
    )

    for s in seeds:
        avatar = generate(
            seed=s,
            size=size,
            corner_radius=radius,
            circle=circle,
            palette=palette,
            filter=filter_opt,
            cat=cat,
            animal=animal,
            mood=mood,
            transparent=transparent,
            shading=shading,
        )
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in s)[:48]
        out_file = output_dir / f"{safe_name}.{ext}"
        avatar.save(out_file, format=ext)
        p_name = avatar.palette.name
        console.print(f"  [green]✓[/green] [bold]{s}[/bold] -> {out_file.name} ({p_name})")

    console.print(f"[bold green]Done![/bold green] All {len(seeds)} avatars generated.")


@app.command(name="iconset", help="Generate a complete web favicon & app icon suite for a seed.")
def iconset_cmd(
    seed: Annotated[
        str,
        typer.Argument(
            help="Seed value for the icon suite.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory to save the icon suite.",
        ),
    ] = Path("./icons"),
    palette: Annotated[
        str | None,
        typer.Option(
            "--palette",
            "-p",
            help="Explicit color palette.",
        ),
    ] = None,
    circle: Annotated[
        bool,
        typer.Option(
            "--circle",
            "-c",
            help="Clip icons to a circular shape.",
        ),
    ] = False,
    transparent: Annotated[
        bool,
        typer.Option(
            "--transparent/--no-transparent",
            help="Render icons with a transparent background.",
        ),
    ] = False,
    cat: Annotated[
        bool | None,
        typer.Option(
            "--cat/--no-cat",
            help="Force cute cat robot features.",
        ),
    ] = None,
    mood: Annotated[
        str | None,
        typer.Option(
            "--mood",
            "-m",
            help="Expression preset: 'happy', 'cool', 'love', 'surprised', 'wink', etc.",
        ),
    ] = None,
) -> None:
    """Generate favicon.ico, apple-touch-icon, chrome icons, SVG, and webmanifest."""
    avatar = generate(
        seed=seed,
        palette=palette,
        circle=circle,
        transparent=transparent,
        cat=cat,
        mood=mood,
        size=512,
    )
    results = avatar.save_iconset(output_dir)

    console.print(
        f"[bold green]✓ Web Icon Suite generated in [cyan]{output_dir}/[/cyan]:[/bold green]"
    )
    for fname, fpath in results.items():
        console.print(f"  • [bold]{fname}[/bold] ({fpath.stat().st_size} bytes)")


@app.command(name="preview", help="Preview robot avatar details and anatomy in terminal.")
def preview_cmd(
    seed: Annotated[
        str | None,
        typer.Argument(
            help="Seed value to inspect. If omitted, a random seed is used.",
        ),
    ] = None,
    palette: Annotated[
        str | None,
        typer.Option(
            "--palette",
            "-p",
            help="Explicit color palette.",
        ),
    ] = None,
    filter_opt: Annotated[
        str | None,
        typer.Option(
            "--filter",
            "-F",
            help="Retro style or filter to apply.",
        ),
    ] = None,
    cat: Annotated[
        bool | None,
        typer.Option(
            "--cat/--no-cat",
            help="Force cute cat robot features.",
        ),
    ] = None,
    animal: Annotated[
        str | None,
        typer.Option(
            "--animal",
            "-a",
            help="Animal preset: 'cat', 'bunny', 'bear'.",
        ),
    ] = None,
    mood: Annotated[
        str | None,
        typer.Option(
            "--mood",
            "-m",
            help="Expression preset: 'happy', 'cool', 'love', 'surprised', 'wink', etc.",
        ),
    ] = None,
    shading: Annotated[
        bool,
        typer.Option(
            "--shading/--no-shading",
            help="Enable or disable 3D cel-shading.",
        ),
    ] = True,
) -> None:
    """Inspect the generated features and colors for a given seed."""
    avatar = generate(
        seed=seed,
        palette=palette,
        filter=filter_opt,
        cat=cat,
        animal=animal,
        mood=mood,
        shading=shading,
    )
    a = avatar.anatomy
    p = avatar.palette

    table = Table(title=f"🤖 Bot Face Anatomy — Seed: '{avatar.seed}'", show_header=False)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Palette", f"{p.name} — {p.description}")
    if filter_opt:
        table.add_row("Filter", filter_opt)
    if mood:
        table.add_row("Mood Preset", mood)
    table.add_row("Head Style", a.head_style.replace("_", " ").title())
    table.add_row("Faceplate", a.faceplate_style.replace("_", " ").title())
    table.add_row("Eyes / Eyewear", a.eye_style.replace("_", " ").title())
    table.add_row("Mouth", a.mouth_style.replace("_", " ").title())
    table.add_row("Antenna", a.antenna_style.replace("_", " ").title())
    table.add_row("Torso", a.torso_style.replace("_", " ").title())
    table.add_row("Chest Badge", a.badge_style.replace("_", " ").title())
    table.add_row("Hat", a.hat_style.replace("_", " ").title())
    table.add_row("Cheeks", a.cheek_style.replace("_", " ").title())
    table.add_row("Whiskers", "Yes" if a.has_whiskers else "No")
    table.add_row("Background", a.background_style.replace("_", " ").title())

    console.print(table)


@app.command(name="palettes", help="List all available bright color palettes.")
def palettes_cmd() -> None:
    """List available color palettes with descriptions."""
    table = Table(title="🎨 Bright Bot-Face Palettes", header_style="bold magenta")
    table.add_column("Name", style="bold cyan", width=18)
    table.add_column("Description", style="white")
    table.add_column("Key Swatches", style="bold yellow")

    for name in list_palettes():
        pal = PALETTES[name]
        swatches = f"{pal.background} | {pal.chassis} | {pal.accent} | {pal.eye_primary}"
        table.add_row(name, pal.description, swatches)

    console.print(table)


@app.command(name="filters", help="List all available retro styles and filters.")
def filters_cmd() -> None:
    """List available retro styles (8-bit, 16-bit, gameboy, CRT, etc.)."""
    table = Table(title="🕹️ Bot-Face Styles & Filters", header_style="bold magenta")
    table.add_column("Filter", style="bold cyan", width=18)
    table.add_column("Description", style="white")

    for name in list_filters():
        table.add_row(name, AVAILABLE_FILTERS[name])

    console.print(table)


@app.command(name="moods", help="List all available robot mood and expression presets.")
def moods_cmd() -> None:
    """List available mood presets (happy, cool, love, surprised, wink, sleepy, neutral)."""
    table = Table(title="🎭 Bot-Face Mood & Expression Presets", header_style="bold magenta")
    table.add_column("Mood", style="bold cyan", width=14)
    table.add_column("Expression & Anatomy Focus", style="white")

    mood_details = {
        "happy": "Smiling mouth (^ ^ or open grin) + rosy blushing cheeks",
        "cool": "Dark sunglasses / cyclops visor + calm smile",
        "love": "Glowing heart LED matrix eyes (♥ ♥) + heart blush + heart chest badge",
        "surprised": "Wide lens eyes (O O) + cute open mouth (:o) + lightbulb idea antenna",
        "wink": "Playful wink eye + cute cat/vamp mouth + rosy blush",
        "sleepy": "Half-closed LED dots/slits + oscilloscope snooze wave + dash blush",
        "neutral": "Glossy pupil lenses + speaker grill mouth",
    }

    for name in MOOD_PRESETS:
        desc = mood_details.get(name, "Expression preset")
        table.add_row(name, desc)

    console.print(table)


@app.command(name="__complete", hidden=True)
def complete_cmd(
    target: Annotated[str, typer.Argument(help="Completion target, e.g. 'spg'.")],
    index: Annotated[int, typer.Argument(help="0-indexed cursor position in original words.")],
    words: Annotated[list[str], typer.Argument(help="Words in the command line.")],
) -> None:
    """Internal completion dispatcher invoked by spg completion hooks."""
    if target == "spg":
        from bot_face.completion_spg import run as spg_run

        spg_run(index, words)


def main() -> None:
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()

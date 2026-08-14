"""Command-line interface for bot-face cute robot avatar generator."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

import bot_face
from bot_face.colors import PALETTES, get_palette, list_palettes
from bot_face.filters import AVAILABLE_FILTERS, list_filters
from bot_face.generator import generate

app = typer.Typer(
    name="bot-face",
    help="🤖 Cute robot avatar generator library and CLI for account profile images.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
err_console = Console(stderr=True)


def version_callback(value: bool) -> None:
    if value:
        v = bot_face.__version__
        console.print(f"[bold cyan]bot-face[/bold cyan] version [green]{v}[/green]")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show the bot-face version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    pass


@app.command(name="generate", help="Generate a cute robot avatar from a seed.")
def generate_cmd(
    seed: Annotated[
        str | None,
        typer.Argument(
            help="Seed value for deterministic generation. If omitted, a random seed is used.",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output path (e.g. avatar.png, avatar.svg). Inferred from extension.",
        ),
    ] = None,
    format_opt: Annotated[
        str | None,
        typer.Option(
            "--format",
            "-f",
            help="Output image format: 'png', 'svg', 'webp', 'jpg'.",
        ),
    ] = None,
    size: Annotated[
        int,
        typer.Option(
            "--size",
            "-s",
            help="Image width and height in pixels.",
            min=16,
            max=4096,
        ),
    ] = 256,
    radius: Annotated[
        int,
        typer.Option(
            "--radius",
            "-r",
            help="Corner radius in pixels for rounded corners.",
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

    avatar = generate(
        seed=seed,
        size=size,
        corner_radius=radius,
        circle=circle,
        palette=palette,
        filter=filter_opt,
        has_hat=hat,
        has_glasses=glasses,
        has_badge=badge,
        cat=cat,
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
        f_info = f", filter: {filter_opt}" if filter_opt else ""
        console.print(
            f"[green]✓[/green] Saved avatar for seed [bold cyan]'{avatar.seed}'[/bold cyan] "
            f"to [bold]{saved_path}[/bold] ([yellow]{pal_name}[/yellow]{f_info}, {size}x{size}px)"
        )
        return

    # If no output path and format is SVG, output to stdout
    if format_opt == "svg":
        console.print(avatar.to_svg(), highlight=False)
        return

    # Default fallback: save to local png file with seed name
    safe_seed = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(avatar.seed))[:32]
    default_out = Path(f"bot_face_{safe_seed}.png")
    saved_path = avatar.save(default_out, format="png")
    pal_name = avatar.palette.name
    f_info = f", filter: {filter_opt}" if filter_opt else ""
    console.print(
        f"[green]✓[/green] Generated avatar for seed [bold cyan]'{avatar.seed}'[/bold cyan] "
        f"-> [bold]{saved_path}[/bold] ([yellow]{pal_name}[/yellow]{f_info}, {size}x{size}px)"
    )


@app.command(name="batch", help="Generate robot avatars for multiple seeds in batch.")
def batch_cmd(
    seeds: Annotated[
        list[str],
        typer.Argument(
            help="List of seeds (usernames, IDs, emails) to generate avatars for.",
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-d",
            help="Directory to save generated avatar files.",
        ),
    ] = Path("avatars"),
    format_opt: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="Output image format: 'png', 'svg', 'webp'.",
        ),
    ] = "png",
    size: Annotated[
        int,
        typer.Option(
            "--size",
            "-s",
            help="Image width and height in pixels.",
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
            shading=shading,
        )
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in s)[:48]
        out_file = output_dir / f"{safe_name}.{ext}"
        avatar.save(out_file, format=ext)
        p_name = avatar.palette.name
        console.print(f"  [green]✓[/green] [bold]{s}[/bold] -> {out_file.name} ({p_name})")

    console.print(f"[bold green]Done![/bold green] All {len(seeds)} avatars generated.")


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
    shading: Annotated[
        bool,
        typer.Option(
            "--shading/--no-shading",
            help="Enable or disable 3D cel-shading.",
        ),
    ] = True,
) -> None:
    """Inspect the generated features and colors for a given seed."""
    avatar = generate(seed=seed, palette=palette, filter=filter_opt, cat=cat, shading=shading)
    a = avatar.anatomy
    p = avatar.palette

    table = Table(title=f"🤖 Bot Face Anatomy — Seed: '{avatar.seed}'", show_header=False)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")

    table.add_row("Palette", f"{p.name} — {p.description}")
    if filter_opt:
        table.add_row("Filter", filter_opt)
    table.add_row("Head Style", a.head_style.replace("_", " ").title())
    table.add_row("Faceplate", a.faceplate_style.replace("_", " ").title())
    table.add_row("Eyes / Eyewear", a.eye_style.replace("_", " ").title())
    table.add_row("Mouth", a.mouth_style.replace("_", " ").title())
    table.add_row("Antenna", a.antenna_style.replace("_", " ").title())
    table.add_row("Torso", a.torso_style.replace("_", " ").title())
    table.add_row("Chest Badge", a.badge_style.replace("_", " ").title())
    table.add_row("Hat", a.hat_style.replace("_", " ").title())
    table.add_row("Cheeks", a.cheek_style.replace("_", " ").title())
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

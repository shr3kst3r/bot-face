"""Tests for the bot-face CLI commands."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from bot_face.cli import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "bot-face version" in result.output


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Cute robot avatar generator" in result.output


def test_cli_palettes() -> None:
    result = runner.invoke(app, ["palettes"])
    assert result.exit_code == 0
    assert "bubblegum" in result.output
    assert "cyber_mint" in result.output


def test_cli_filters() -> None:
    result = runner.invoke(app, ["filters"])
    assert result.exit_code == 0
    assert "8bit" in result.output
    assert "gameboy" in result.output


def test_cli_preview() -> None:
    result = runner.invoke(app, ["preview", "super_robot", "--filter", "8bit"])
    assert result.exit_code == 0
    assert "Bot Face Anatomy" in result.output
    assert "super_robot" in result.output
    assert "8bit" in result.output


def test_cli_generate_with_filter(tmp_path: Path) -> None:
    out_file = tmp_path / "bot_8bit.png"
    result = runner.invoke(
        app,
        ["generate", "my_seed", "--output", str(out_file), "--filter", "8bit"],
    )
    assert result.exit_code == 0
    assert out_file.exists()


def test_cli_generate_cat(tmp_path: Path) -> None:
    out_file = tmp_path / "cat_bot.png"
    result = runner.invoke(app, ["generate", "cat_lover", "--cat", "--output", str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()


def test_cli_generate_invalid_filter() -> None:
    result = runner.invoke(app, ["generate", "seed", "--filter", "bad_filter"])
    assert result.exit_code == 1
    assert "Unknown filter" in result.output


def test_cli_completion_spg() -> None:
    result = runner.invoke(app, ["__complete", "spg", "1", "generate"])
    assert result.exit_code == 0


def test_cli_generate_file(tmp_path: Path) -> None:
    out_file = tmp_path / "custom_bot.png"
    result = runner.invoke(
        app,
        ["generate", "my_seed", "--output", str(out_file), "--size", "128", "--radius", "16"],
    )
    assert result.exit_code == 0
    assert out_file.exists()
    assert "Saved avatar for seed" in result.output


def test_cli_generate_svg_stdout() -> None:
    result = runner.invoke(app, ["generate", "stdout_seed", "--format", "svg"])
    assert result.exit_code == 0
    assert "<svg" in result.output


def test_cli_generate_data_uri() -> None:
    result = runner.invoke(app, ["generate", "uri_seed", "--data-uri"])
    assert result.exit_code == 0
    assert "data:image/svg+xml;base64," in result.output


def test_cli_generate_invalid_palette() -> None:
    result = runner.invoke(app, ["generate", "seed", "--palette", "nonexistent_palette"])
    assert result.exit_code == 1
    assert "Unknown palette" in result.output


def test_cli_batch(tmp_path: Path) -> None:
    out_dir = tmp_path / "batch_out"
    result = runner.invoke(
        app,
        ["batch", "user_1", "user_2", "user_3", "--output-dir", str(out_dir), "--format", "png"],
    )
    assert result.exit_code == 0
    assert (out_dir / "user_1.png").exists()
    assert (out_dir / "user_2.png").exists()
    assert (out_dir / "user_3.png").exists()
    assert "All 3 avatars generated" in result.output

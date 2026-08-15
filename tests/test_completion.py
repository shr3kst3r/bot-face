"""Tests for the spg tab completion dispatcher."""

from __future__ import annotations

from bot_face.completion_spg import (
    _clean,
    _short,
    run,
)


def test_clean_and_short() -> None:
    assert _clean("foo:bar\nbaz") == "foo —bar baz"
    assert _short("line1\nline2") == "line1"
    assert _short("") == ""


def test_completion_spg_run(capsys) -> None:  # type: ignore[no-untyped-def]
    # Complete subcommands
    run(1, [""])
    captured = capsys.readouterr()
    assert "generate" in captured.out
    assert "palettes" in captured.out
    assert "filters" in captured.out


def test_completion_spg_flags(capsys) -> None:  # type: ignore[no-untyped-def]
    # Complete flags for generate
    run(2, ["generate", "-"])
    captured = capsys.readouterr()
    assert "--palette" in captured.out or "-p" in captured.out
    assert "--filter" in captured.out or "-F" in captured.out


def test_completion_spg_option_values(capsys) -> None:  # type: ignore[no-untyped-def]
    # Complete values for --palette
    run(3, ["generate", "--palette", ""])
    captured = capsys.readouterr()
    assert "bubblegum" in captured.out

    # Complete values for --filter
    run(3, ["generate", "--filter", ""])
    captured = capsys.readouterr()
    assert "8bit" in captured.out
    assert "gameboy" in captured.out

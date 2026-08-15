"""Completion hook implementing spg's contract for the `bot-face` / `bf` command."""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

import typer

from bot_face.colors import list_palettes
from bot_face.filters import list_filters

_FILES_SENTINEL = "__files__"
_DIRS_SENTINEL = "__directories__"

_OPTION_VALUE_ENUMERATORS: dict[str, Callable[[], list[str]]] = {
    "--palette": list_palettes,
    "-p": list_palettes,
    "--filter": list_filters,
    "-F": list_filters,
    "--format": lambda: ["png", "svg", "webp", "jpg"],
    "-f": lambda: ["png", "svg", "webp", "jpg"],
}

_POSITIONAL_ENUMERATORS: dict[str, Callable[[], list[str]]] = {}


def run(
    index: int,
    words_after_cmd: list[str],
    subcommand: tuple[str, ...] = (),
) -> None:
    """Emit spg-formatted candidates for cursor at `index` in original words."""
    from bot_face.cli import app as bf_app

    root = typer.main.get_command(bf_app)
    if not hasattr(root, "commands"):
        return

    start: Any = root
    for part in subcommand:
        if not hasattr(start, "commands"):
            return
        nxt = start.commands.get(part)
        if nxt is None:
            return
        start = nxt

    tab_idx = max(0, index - 1)
    current, consumed_positionals = _walk(start, words_after_cmd, tab_idx)

    cur_word = words_after_cmd[tab_idx] if tab_idx < len(words_after_cmd) else ""
    prev_word = (
        words_after_cmd[tab_idx - 1] if tab_idx > 0 and tab_idx - 1 < len(words_after_cmd) else ""
    )

    if prev_word.startswith("-"):
        opt = _find_option(current, prev_word)
        if opt is not None and not _is_flag_only(opt):
            _emit_option_values(opt)
            return

    if cur_word.startswith("-"):
        _emit_flags(current)
        return

    if hasattr(current, "commands"):
        _emit_subcommands(current)
        return

    _emit_positional(current, consumed_positionals)
    _emit_flags(current)


def _walk(
    root: Any,
    words_after_cmd: list[str],
    tab_idx: int,
) -> tuple[Any, int]:
    current: Any = root
    consumed_positionals = 0
    i = 0
    while i < tab_idx and i < len(words_after_cmd):
        word = words_after_cmd[i]
        if hasattr(current, "commands") and not word.startswith("-") and word in current.commands:
            current = current.commands[word]
            consumed_positionals = 0
            i += 1
            continue
        if word.startswith("-"):
            if "=" in word:
                i += 1
                continue
            opt = _find_option(current, word)
            if opt is not None and not _is_flag_only(opt):
                i += 2
                continue
            i += 1
            continue
        consumed_positionals += 1
        i += 1
    return current, consumed_positionals


def _find_option(cmd: Any, flag: str) -> Any:
    if not hasattr(cmd, "params"):
        return None
    for p in cmd.params:
        opts = list(getattr(p, "opts", []) or []) + list(getattr(p, "secondary_opts", []) or [])
        if flag in opts:
            return p
    return None


def _is_flag_only(opt: Any) -> bool:
    return bool(getattr(opt, "is_flag", False)) or bool(getattr(opt, "count", False))


def _emit_subcommands(group: Any) -> None:
    commands_dict = getattr(group, "commands", {})
    for name in sorted(commands_dict):
        cmd = commands_dict[name]
        if getattr(cmd, "hidden", False):
            continue
        _emit(name, _short(getattr(cmd, "short_help", "") or getattr(cmd, "help", "") or ""))


def _emit_flags(cmd: Any) -> None:
    for param in getattr(cmd, "params", []):
        help_text = _short(getattr(param, "help", "") or "")
        opts = list(getattr(param, "opts", []) or []) + list(
            getattr(param, "secondary_opts", []) or []
        )
        for flag in opts:
            _emit(flag, help_text)


def _emit_option_values(opt: Any) -> None:
    opt_type = getattr(opt, "type", None)
    if hasattr(opt_type, "choices"):
        for c in opt_type.choices:
            _emit(str(c), "")
        return
    for flag in getattr(opt, "opts", []):
        if flag in _OPTION_VALUE_ENUMERATORS:
            for v in _OPTION_VALUE_ENUMERATORS[flag]():
                _emit(v, "")
            return


def _emit_positional(cmd: Any, slot: int) -> None:
    params = getattr(cmd, "params", [])
    args = [p for p in params if hasattr(p, "name") and not getattr(p, "opts", None)]
    if slot >= len(args):
        return
    arg = args[slot]
    arg_type = getattr(arg, "type", None)
    if hasattr(arg_type, "choices"):
        for c in arg_type.choices:
            _emit(str(c), "")
        return
    name = getattr(arg, "name", "") or ""
    if name in _POSITIONAL_ENUMERATORS:
        for v in _POSITIONAL_ENUMERATORS[name]():
            _emit(v, "")


def _emit(value: str, description: str) -> None:
    if description:
        sys.stdout.write(f"{value}:{_clean(description)}\n")
    else:
        sys.stdout.write(f"{value}\n")


def _clean(text: str) -> str:
    return text.replace(":", " —").replace("\n", " ").strip()


def _short(text: str) -> str:
    text = text.strip()
    return text.splitlines()[0] if text else ""

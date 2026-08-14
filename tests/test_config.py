"""Tests for AvatarConfig validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from bot_face.config import AvatarConfig


def test_avatar_config_defaults() -> None:
    cfg = AvatarConfig()
    assert cfg.seed is None
    assert cfg.size == 256
    assert cfg.corner_radius == 0
    assert cfg.circle is False
    assert cfg.palette is None


def test_avatar_config_custom() -> None:
    cfg = AvatarConfig(
        seed="user123",
        size=512,
        corner_radius=32,
        circle=True,
        palette="cyber_mint",
        has_hat=True,
        has_glasses=False,
        has_badge=True,
    )
    assert cfg.seed == "user123"
    assert cfg.size == 512
    assert cfg.corner_radius == 32
    assert cfg.circle is True
    assert cfg.palette == "cyber_mint"
    assert cfg.has_hat is True
    assert cfg.has_glasses is False
    assert cfg.has_badge is True


def test_avatar_config_validation_errors() -> None:
    with pytest.raises(ValidationError):
        AvatarConfig(size=8)  # ge=16

    with pytest.raises(ValidationError):
        AvatarConfig(size=5000)  # le=4096

    with pytest.raises(ValidationError):
        AvatarConfig(corner_radius=-5)  # ge=0

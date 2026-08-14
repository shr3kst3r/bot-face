"""Shared pytest fixtures for bot-face tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_seeds() -> list[str]:
    return ["alice@example.com", "bob_the_builder", "charlie-99", "robot-007", "42"]

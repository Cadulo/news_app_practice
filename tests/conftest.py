"""Pytest configuration."""

import pytest


@pytest.fixture  # type: ignore[misc]
def anyio_backend() -> str:
    """Use asyncio as the AnyIO backend."""
    return "asyncio"

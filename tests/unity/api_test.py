"""Test the main module."""
from importlib import metadata

import toml
from pytest import fixture

from api import settings
from src.api import database, environment, main, users, utils


def test_version() -> None:
    """Test version."""
    app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    assert main.version()["version"] == app_version

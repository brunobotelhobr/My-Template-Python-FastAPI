"""Test the main module."""
from pytest import fixture
from importlib import metadata
import toml

from src.api import main, config, environment, users, utils, database

def test_version() -> None:
    """Test version."""
    app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    assert main.version()["version"] == app_version



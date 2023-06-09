"""temp."""
import re

import pytest
import toml  # type: ignore
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.order(3)
def test_health() -> None:
    """Test the health."""
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.order(3)
def test_not_found() -> None:
    """Test the not found."""
    response = client.get("/not-found")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.order(3)
def test_docs() -> None:
    """Test the docs."""
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.order(3)
def test_openapi() -> None:
    """Test the openapi."""
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_redoc() -> None:
    """Test the redoc."""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_version() -> None:
    """Test the version."""
    version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": version}
    assert re.match(r"\d+\.\d+\.\d+", version)

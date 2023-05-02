"""Test the database.py module."""
import pytest

from api.database import init_db


@pytest.mark.order(2)
def init_db_test():
    """Test the database initialization."""
    assert init_db() is True

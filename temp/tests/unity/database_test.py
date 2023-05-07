"""Test the database.py module."""
import pytest

from api.core.database import initialize_database


@pytest.mark.order(2)
def init_db_test():
    """Test the database initialization."""
    assert initialize_database() is True

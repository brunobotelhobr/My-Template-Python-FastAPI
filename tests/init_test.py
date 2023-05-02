import pytest

from api.database import init_db


@pytest.mark.order(1)
def init_test():
    """Test if the database is initialized correctly."""
    assert init_db() is True

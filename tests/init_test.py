"""temp."""
import pytest

from api.core.database import initialize_database


@pytest.mark.order(1)
def init_test():
    """Test if the database is initialized correctly."""
    assert initialize_database() is True

"""temp."""
import unittest

import pytest

from api.settings.schema import SettingsModel
from api.settings.utils import load, reset, save


@pytest.mark.order(2)
class TestUtils(unittest.TestCase):
    """TestCase for settings utils."""

    def test(self):
        """Test load."""
        # Test simple save.
        model = SettingsModel(name="test")
        self.assertEqual(model.name, "test")
        assert save(model) is True
        # Test simple load.
        model.api.get_default_page_size = 123
        assert save(model) is True
        assert load(model) is True
        self.assertEqual(model.api.get_default_page_size, 123)
        model.users.allow_delete = False
        assert save(model) is True
        assert load(model) is True
        self.assertEqual(model.users.allow_delete, False)
        model.users.password_policy.min_length = 10
        assert save(model) is True
        assert load(model) is True
        self.assertEqual(model.users.password_policy.min_length, 10)
        # Test reset.
        assert reset(model) is True
        assert reset(model) is False
        # Load non-existent.
        temp = SettingsModel(name="non-existent")
        assert load(temp) is False

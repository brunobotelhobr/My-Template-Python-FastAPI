import unittest

import pytest

from api.settings.schema import SettingsAPI, SettingsModel
from api.utils import generator


@pytest.mark.order(2)
class TestSettingsAPI(unittest.TestCase):
    """Test SettingsAPI."""

    def test_init(self):
        """Test init."""
        api = SettingsAPI()
        self.assertEqual(api.get_max_page_size, 1000)
        self.assertEqual(api.get_default_page_size, 100)

    def test_validate_get_max_page_size(self):
        """Test validate_get_max_page_size."""
        api = SettingsAPI()
        values = {"get_max_page_size": 500, "get_default_page_size": 100}
        result = api.validate_get_max_page_size(values)
        self.assertEqual(result, values)

    def test_validate_get_max_page_size_fails(self):
        """Test validate_get_max_page_size fails."""
        api = SettingsAPI()
        values = {"get_max_page_size": 0, "get_default_page_size": 100}
        with self.assertRaises(ValueError):
            api.validate_get_max_page_size(values)

        values = {"get_max_page_size": 50, "get_default_page_size": 100}
        with self.assertRaises(ValueError):
            api.validate_get_max_page_size(values)


@pytest.mark.order(2)
class TestSettingsModel(unittest.TestCase):
    """Test SettingsModel."""

    test_name = generator.salt()

    def test_init(self):
        """Test init."""
        model = SettingsModel()
        self.assertEqual(model.name, "global")

        model = SettingsModel(name=self.test_name)
        self.assertEqual(model.name, self.test_name)

        model.users.allow_delete = True
        self.assertEqual(model.users.allow_delete, True)
        model.users.allow_delete = False
        self.assertEqual(model.users.allow_delete, False)

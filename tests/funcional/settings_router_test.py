import unittest

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.settings.schema import SettingsModel


@pytest.mark.order(3)
class TestSettings(unittest.TestCase):
    """Test Settings."""

    client = TestClient(app)

    def test_get_settings(self):
        """Test get_settings."""
        name = "pudim"
        response = self.client.get("/admin/settings/" + name)
        self.assertEqual(response.status_code, 200)
        assert SettingsModel().parse_raw(response.content)

    def test_update_settings(self):
        """Test update_settings."""
        name = "pudim"
        s = SettingsModel(name=name)
        s.api.get_default_page_size = 199
        response = self.client.put("/admin/settings/", json=s.dict())
        self.assertEqual(response.status_code, 200)
        r = SettingsModel().parse_raw(response.content)
        self.assertEqual(r.api.get_default_page_size, 199)
        s.users.allow_delete = False
        response = self.client.put("/admin/settings/", json=s.dict())
        self.assertEqual(response.status_code, 200)
        r = SettingsModel().parse_raw(response.content)
        self.assertEqual(r.users.allow_delete, False)
        s.users.password_policy.min_length = 10
        response = self.client.put("/admin/settings/", json=s.dict())
        self.assertEqual(response.status_code, 200)
        r = SettingsModel().parse_raw(response.content)
        self.assertEqual(r.users.password_policy.min_length, 10)
        # Test invalid settings.
        s = SettingsModel(name="invalid-name-I_do_not_exist")
        response = self.client.put("/admin/settings/", json=s.dict())
        self.assertEqual(response.status_code, 200)

    def test_reset_settings(self):
        """Test reset_settings."""
        name = "pudim"
        s = SettingsModel(name=name)
        s.api.get_default_page_size = 199
        response = self.client.put("/admin/settings/", json=s.dict())
        self.assertEqual(response.status_code, 200)
        r = SettingsModel().parse_raw(response.content)
        self.assertEqual(r.api.get_default_page_size, 199)
        response = self.client.patch("/admin/settings/")
        self.assertEqual(response.status_code, 200)
        r = SettingsModel().parse_raw(response.content)
        self.assertEqual(r.api.get_default_page_size, 100)

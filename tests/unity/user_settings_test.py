import pytest
from pydantic import ValidationError

from api.users.settings import PasswordPolicy, SettingsUser


def test_password_policy():
    """Test PasswordPolicy validator."""
    pp = PasswordPolicy()
    assert pp.active
    assert pp.min_length == 8
    assert pp.max_length == 64
    assert pp.min_upper == 1
    assert pp.min_lower == 1
    assert pp.min_digits == 1
    assert pp.min_special == 1
    assert pp.min_length == 8

    # Validate if min_length can be equal to max_length
    pp = PasswordPolicy(min_length=8, max_length=8)
    assert pp.min_length == 8
    assert pp.max_length == 8

    # Validate neggative values
    with pytest.raises(ValidationError):
        PasswordPolicy(min_upper=-1)

    with pytest.raises(ValidationError):
        PasswordPolicy(min_lower=-1)

    with pytest.raises(ValidationError):
        PasswordPolicy(min_digits=-1)

    with pytest.raises(ValidationError):
        PasswordPolicy(min_special=-1)

    with pytest.raises(ValidationError):
        PasswordPolicy(min_length=-1)

    with pytest.raises(ValidationError):
        PasswordPolicy(max_length=-1)

    # Validate min_length > max_length
    with pytest.raises(ValidationError):
        PasswordPolicy(min_length=9, max_length=8)

    # Validate min_length < sum of min_upper, min_lower, min_digits and min_special
    with pytest.raises(ValidationError):
        PasswordPolicy(min_length=3, min_upper=1, min_lower=1, min_digits=1, min_special=1)

    # Validate max_length > 128
    with pytest.raises(ValidationError):
        PasswordPolicy(max_length=129)


def test_settings_user():
    """Test SettingsUser validator."""
    su = SettingsUser()
    assert su.strickes == 3

    # Validate negative values
    with pytest.raises(ValidationError):
        SettingsUser(strickes=-1)

    # Validate zero value
    with pytest.raises(ValidationError):
        SettingsUser(strickes=0)

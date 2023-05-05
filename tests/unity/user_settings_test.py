"""temp."""
import pytest
from pydantic import ValidationError

from api.users.settings import PasswordPolicy, SettingsUser


@pytest.mark.order(2)
def test_password_policy():
    """Test PasswordPolicy validator."""
    poassword_policy = PasswordPolicy()
    assert poassword_policy.active
    assert poassword_policy.min_length == 8
    assert poassword_policy.max_length == 64
    assert poassword_policy.min_upper == 1
    assert poassword_policy.min_lower == 1
    assert poassword_policy.min_digits == 1
    assert poassword_policy.min_special == 1
    assert poassword_policy.min_length == 8

    # Validate if min_length can be equal to max_length
    poassword_policy = PasswordPolicy(min_length=8, max_length=8)
    assert poassword_policy.min_length == 8
    assert poassword_policy.max_length == 8

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
        PasswordPolicy(
            min_length=3, min_upper=1, min_lower=1, min_digits=1, min_special=1
        )

    # Validate max_length > 128
    with pytest.raises(ValidationError):
        PasswordPolicy(max_length=129)


@pytest.mark.order(2)
def test_settings_user():
    """Test SettingsUser validator."""
    user_settings = SettingsUser()
    assert user_settings.strickes == 3

    # Validate negative values
    with pytest.raises(ValidationError):
        SettingsUser(strickes=-1)

    # Validate zero value
    with pytest.raises(ValidationError):
        SettingsUser(strickes=0)

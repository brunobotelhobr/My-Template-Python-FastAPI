from pydantic import ValidationError
import pytest

from api.users.settings import PasswordPolicy, UserSettings

def test_password_policy_validator():
    """Test PasswordPolicy validator."""
    pp = PasswordPolicy()
    assert pp.active == True
    
    with pytest.raises(ValidationError):
        pp.max_length = -1
        pp.min_length = -1
        pp.min_upper = -1
        pp.min_lower = -1
        pp.min_digits = -1
        pp.min_special = -1
        pp.max_length = 129
        pp.min_length = 129
        pp.min_upper = 129
        pp.min_lower = 129
        pp.min_digits = 129
        pp.min_special = 129

    with pytest.raises(ValueError):
        pp.max_length = 10
        pp.min_length = 11
    
    with pytest.raises(ValueError):
        pp.min_upper = 10
        pp.min_lower = 10
        pp.min_digits = 10
        pp.min_special = 10
        pp.min_length = 10
        pp.max_length = 10
    
    assert pp.max_length == 10
    assert pp.min_length == 10
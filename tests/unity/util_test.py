"""Test utils."""
import string

import pytest
from pytest import raises

from api.utils import generator


@pytest.mark.order(2)
def test_generator():
    """Test generator."""
    assert generator.name()
    assert generator.email()
    assert generator.password()
    assert generator.uuid()
    assert generator.now()
    assert generator.hasher(password=generator.password(), salt=generator.salt())

    # The gnerator, it must degenerate different values
    assert generator.name() != generator.name()
    assert generator.email() != generator.email()
    assert generator.password() != generator.password()
    assert generator.uuid() != generator.uuid()
    assert generator.now() != generator.now()
    assert generator.hasher(password=generator.password(), salt=generator.salt()) != generator.hasher(password=generator.password(), salt=generator.salt())

    # Test the password function, length
    assert len(generator.password(size=10)) == 10
    assert len(generator.password(size=20)) == 20
    assert len(generator.password(size=30)) == 30
    assert len(generator.password(size=40)) == 40

    # validate is password can contains a least x lowercase characters
    assert len([c for c in generator.password(lower=3) if c in string.ascii_lowercase]) >= 3
    assert len([c for c in generator.password(lower=5) if c in string.ascii_lowercase]) >= 5

    # validate is password can contains a least x upercase characters
    assert len([c for c in generator.password(uper=3) if c in string.ascii_uppercase]) >= 3
    assert len([c for c in generator.password(uper=5) if c in string.ascii_uppercase]) >= 5

    # validate is password can contains a least x special characters
    assert len([c for c in generator.password(special=3) if c in string.punctuation]) >= 3
    assert len([c for c in generator.password(special=5) if c in string.punctuation]) >= 5

    # validate is password can contains a least x numbers
    assert len([c for c in generator.password(numbers=3) if c in string.digits]) >= 3
    assert len([c for c in generator.password(numbers=5) if c in string.digits]) >= 5

    # validate is password can contains a least x numbers, special, uper and lower
    assert len([c for c in generator.password(numbers=3, special=3, uper=3, lower=3) if c in string.digits]) >= 3

    # validate exceptions
    with raises(ValueError):
        generator.password(size=-1)

    with raises(ValueError):
        generator.password(size=10, numbers=-1)

    with raises(ValueError):
        generator.password(size=10, special=-1)

    with raises(ValueError):
        generator.password(size=10, uper=-1)

    with raises(ValueError):
        generator.password(size=10, lower=-1)

    with raises(ValueError):
        generator.password(size=10, numbers=5, special=5, uper=5, lower=5)

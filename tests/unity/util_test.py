from time import sleep
from pytest import raises

from api.utils import generator


def test_generator():
    """Test generator."""
    assert generator.name()
    assert generator.email()
    assert generator.password()
    assert generator.uuid()
    assert generator.now()
    assert generator.hasher(password=generator.password(), salt=generator.salt())

    # Test random values
    with raises(ValueError):
        firt_name = generator.name()
        second_name = generator.name()
        if firt_name == second_name:
            raise ValueError("The names are the same")

    with raises(ValueError):
        firt_email = generator.email()
        second_email = generator.email()
        if firt_email == second_email:
            raise ValueError("The emails are the same")

    with raises(ValueError):
        firt_password = generator.password()
        second_password = generator.password()
        if firt_password == second_password:
            raise ValueError("The passwords are the same")

    with raises(ValueError):
        firt_uuid = generator.uuid()
        sleep(0.1)
        second_uuid = generator.uuid()
        if firt_uuid == second_uuid:
            raise ValueError("The uuids are the same")

    with raises(ValueError):
        firt_now = generator.now()
        second_now = generator.now()
        if firt_now == second_now:
            raise ValueError("The nows are the same")

    with raises(ValueError):
        firt_hasher = generator.hasher(password=generator.password(), salt=generator.salt())
        second_hasher = generator.hasher(password=generator.password(), salt=generator.salt())
        if firt_hasher == second_hasher:
            raise ValueError("The hashers are the same")


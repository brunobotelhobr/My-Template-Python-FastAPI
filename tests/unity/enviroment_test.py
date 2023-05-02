import pytest

from api.environment import DatabaseSettings, Environment, RunnigeEnviroment


@pytest.mark.order(2)
@pytest.mark.parametrize(
    "env, expected_debug, expected_testing, expected_deployed",
    [
        (Environment.LOCAL, True, False, False),
        (Environment.STAGING, True, False, True),
        (Environment.TESTING, True, True, False),
        (Environment.PRODUCTION, False, False, True),
    ],
)
def test_is_debug_testing_deployed(env, expected_debug, expected_testing, expected_deployed):
    """Test the is_debug, is_testing and is_deployed properties of the Environment enum."""
    assert env.is_debug == expected_debug
    assert env.is_testing == expected_testing
    assert env.is_deployed == expected_deployed


@pytest.mark.order(2)
def test_database_settings():
    """Test the DatabaseSettings class."""
    database = DatabaseSettings()
    assert database.url == "sqlite:///database.db"
    assert database.aut_create_models is True


@pytest.mark.order(2)
def test_running_environment():
    """Test the RunnigeEnviroment class."""
    env = RunnigeEnviroment()
    assert env.local == Environment.LOCAL

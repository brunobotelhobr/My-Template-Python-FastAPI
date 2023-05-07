"""temp."""
import pytest

from api.core.environment import (
    DatabaseEnvironment,
    EnvironmentBehavior,
    RunnigeEnviroment,
)


@pytest.mark.order(2)
@pytest.mark.parametrize(
    "env, expected_debug, expected_testing, expected_deployed",
    [
        (EnvironmentBehavior.LOCAL, True, False, False),
        (EnvironmentBehavior.STAGING, True, False, True),
        (EnvironmentBehavior.TESTING, True, True, False),
        (EnvironmentBehavior.PRODUCTION, False, False, True),
    ],
)
def test_is_debug_testing_deployed(
    env, expected_debug, expected_testing, expected_deployed
):
    """Test the is_debug, is_testing and is_deployed properties of the EnvironmentBehavior enum."""
    assert env.is_debug == expected_debug
    assert env.is_testing == expected_testing
    assert env.is_deployed == expected_deployed


@pytest.mark.order(2)
def test_database_settings():
    """Test the DatabaseEnvironment class."""
    database = DatabaseEnvironment()
    assert database.database_connection_url == "sqlite:///database.db"
    assert database.aut_create_models is True


@pytest.mark.order(2)
def test_running_environment():
    """Test the RunnigeEnviroment class."""
    env = RunnigeEnviroment()
    assert env.local == EnvironmentBehavior.LOCAL

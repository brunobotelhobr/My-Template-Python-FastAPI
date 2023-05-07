"""Settings Utils Module."""
from api.core.settings.schema import RunningSettings


def get_running_settings() -> RunningSettings:
    """Get the running settings."""
    if RunningSettings().load() is False:
        raise ValueError("Settings not loaded")
    return RunningSettings()

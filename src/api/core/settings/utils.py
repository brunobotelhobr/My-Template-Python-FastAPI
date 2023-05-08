"""Settings Utils Module."""
from api.core.settings.model import RunningSettings, Settings


def get_running_settings() -> RunningSettings:
    """Get the running settings."""
    if RunningSettings().load() is False:
        raise ValueError("Settings not loaded")
    return RunningSettings()


def get_settings() -> Settings:
    """Get the settings."""
    return Settings()


running_settings = get_running_settings()
settings = get_settings()

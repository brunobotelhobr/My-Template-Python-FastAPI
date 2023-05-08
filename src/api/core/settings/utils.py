"""Settings Utils Module."""
from api.core.settings.model import RunningSettings, Settings

settings = Settings()
running_settings = RunningSettings()
# Load settings from database
running_settings.load()


def get_running_settings() -> RunningSettings:
    """Get the running settings."""
    if RunningSettings().load() is False:
        raise ValueError("Settings not loaded")
    return RunningSettings()


def get_settings() -> Settings:
    """Get the settings."""
    return Settings()

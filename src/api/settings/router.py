"""Settings router."""
from fastapi import APIRouter, status

from api.core.dependencies import Settings
from api.settings.schema import SettingsGlobal

router = APIRouter()


@router.get("/", response_model=SettingsGlobal, status_code=status.HTTP_200_OK)
async def get_settings(settings: Settings):
    """Get the application settings."""
    return settings


@router.patch("/", response_model=SettingsGlobal, status_code=status.HTTP_200_OK)
async def update_settings(settings: Settings, settings_in: SettingsGlobal):
    """Update the application settings."""
    for item, value in settings_in.dict().items():
        setattr(settings, item, value)
        settings.save()
    return settings


@router.put("/", response_model=SettingsGlobal, status_code=status.HTTP_200_OK)
async def reset_settings(
    settings: Settings,
):
    """Reset the application settings."""
    new_settings = SettingsGlobal()
    new_settings.save()
    settings = new_settings
    return settings

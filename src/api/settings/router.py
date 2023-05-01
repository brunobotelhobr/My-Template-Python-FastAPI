from fastapi import APIRouter

from api.settings.schema import SettingsModel

router = APIRouter()

settings = SettingsModel()


@router.get("/settings", response_model=SettingsModel)
async def get_settings():
    """Get the application settings."""
    return settings


@router.patch("/settings", response_model=SettingsModel)
async def update_settings(c: SettingsModel):
    """Update the application settings."""
    c.save()
    settings.load()
    return settings

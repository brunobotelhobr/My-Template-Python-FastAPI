from fastapi import APIRouter

from api.settings.schema import SettingsModel
from api.settings.utils import load, reset, save

router = APIRouter()

settings = SettingsModel()


@router.get("/", response_model=SettingsModel)
async def get_settings(name: str = "global"):
    """Get the application settings."""
    s = SettingsModel(name=name)
    load(s)
    return s


@router.patch("/", response_model=SettingsModel)
async def update_settings(name: str = "global", settings: SettingsModel = settings):
    """Update the application settings."""
    if settings.name != name:
        settings.name = name
    save(settings=settings)
    return settings


@router.put("/", response_model=SettingsModel)
async def reset_settings(name: str = "global"):
    """Reset the application settings."""
    s = SettingsModel(name=name)
    reset(settings=s)
    return s

from fastapi import APIRouter, status

from api.settings.schema import SettingsModel
from api.settings.utils import load, reset, save
from api.settings.router import settings

router = APIRouter()


@router.get("/", response_model=SettingsModel, status_code=status.HTTP_200_OK)
async def get_settings(name: str = "global"):
    """Get the application settings."""
    s = SettingsModel(name=name)
    load(s)
    return s


@router.patch("/", response_model=SettingsModel, status_code=status.HTTP_200_OK)
async def update_settings(name: str = "global", s: SettingsModel = settings):
    """Update the application settings."""
    if s.name != name:
        s.name = name
    save(settings=s)
    return s


@router.put("/", response_model=SettingsModel, status_code=status.HTTP_200_OK)
async def reset_settings(name: str = "global"):
    """Reset the application settings."""
    s = SettingsModel(name=name)
    reset(settings=s)
    return s

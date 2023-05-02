from fastapi import APIRouter

from api.settings.schema import SettingsModel
from api.settings.utils import load, save

router = APIRouter()

settings = SettingsModel()


@router.get("/{name}", response_model=SettingsModel)
async def get_settings(name: str = "global"):
    """Get the application settings."""
    s = SettingsModel(name=name)
    load(s)
    return s


@router.put("/", response_model=SettingsModel)
async def update_settings(s: SettingsModel):
    """Update the application settings."""
    save(s)
    return s


@router.patch("/", response_model=SettingsModel)
async def reset_settings(name: str = "global"):
    """Reset the application settings."""
    s = SettingsModel(name=name)
    save(s)
    return s

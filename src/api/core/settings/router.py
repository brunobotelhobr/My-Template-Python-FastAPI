"""Settings router."""
from fastapi import APIRouter, HTTPException, status

from api.core.settings.schema import RunningSettings

router = APIRouter()


@router.get(
    "/",
    response_model=RunningSettings,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        500: {"description": "Internal Server Error."},
    },
)
async def get_settings():
    """
    Get Settings.

    Get the application settings.

    Returns:
        RunningSettings: Application settings.
    """
    return RunningSettings()


@router.patch(
    "/",
    response_model=RunningSettings,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        500: {"description": "Internal Server Error."},
    },
)
async def update_settings(settings_in: RunningSettings):
    """
    Patch Settings.

    Update the application settings.

    Args:
        settings_in (RunningSettings): Application settings.

    Returns:
        RunningSettings: Application settings.
    """
    for item, value in settings_in.dict().items():
        setattr(RunningSettings(), item, value)
    if RunningSettings().save() is True:
        return RunningSettings()
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
    )


@router.get(
    "/reset",
    response_model=RunningSettings,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        500: {"description": "Internal Server Error."},
    },
)
async def reset_settings():
    """
    Reset Settings.

    Reset the application settings to default.

    Returns:
        RunningSettings: Application settings.
    """
    if RunningSettings().reset() is True:
        return RunningSettings()
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
    )

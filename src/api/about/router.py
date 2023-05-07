"""About router."""
from fastapi import APIRouter, status

from api.core.constants import app_version

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful Response."},
        500: {"description": "Internal Server Error."},
    },
)
def version() -> dict[str, str]:
    """
    Get the Version of the Application.

    Returns:
        dict[str, str]: Version of the Application.
    """
    return {"version": app_version}

"""About router."""
from fastapi import APIRouter, status

from api.core.constants import app_version

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def version() -> dict[str, str]:
    """Version endpoint for the API."""
    return {"version": app_version}

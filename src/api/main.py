"""Main module for the API."""
import toml  # type: ignore
from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.auth.router import authenticate
from api.auth.router import router as auth_router
from api.database import init_db
from api.environment import db, env
from api.settings.router import router as settings_router
from api.settings.router import settings
from api.settings.utils import load, save
from api.users.router import router as user_router
from api.users.schema import UserOut
from api.database import get_db
from sqlalchemy.orm import Session

# Get app name and version from pyproject.toml
app_name = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

# Create FastAPI instance
app = FastAPI(title=app_name, version=app_version, debug=env.local.is_debug)

# Adjust interactive documentation
if env.local.is_debug is True:
    app.redoc_url = "/redoc"
    app.openapi_url = "/openapi.json"
    app.docs_url = "/docs"
else:
    app.redoc_url = None
    app.openapi_url = None
    app.docs_url = None


# On Startup event
@app.on_event("startup")
async def startup() -> None:
    """Triggered when the application is starting up."""
    # Check if the environment is initialized
    if env is None:
        raise ValueError("Enviroment not initialized")
    if db is None:
        raise ValueError("Database settings not initialized")
    # Initialize database, if debug mode is enabled
    if env.local.is_debug:
        init_db()
    # Load settings, if not exists, create it
    if load(settings=settings) is False:
        save(settings=settings)

# On Shutdown event
@app.on_event("shutdown")
async def shutdown() -> None:
    """Triggered when the application is shutting down."""
    ...

# Healthcheck endpoint
@app.get("/healthcheck", include_in_schema=False)
async def healthcheck(database: Session = Depends(get_db)) -> dict[str, str]:
    """Healthcheck endpoint for load balancers."""
    return {"status": "error"}


@app.get("/version", tags=["About"])
def version() -> dict[str, str]:
    """Version endpoint for the API."""
    return {"version": app_version}


@app.get("/me", tags=["Me"], response_model=UserOut)
def me(who: UserOut = Depends(authenticate)) -> UserOut:
    """Me endpoint for the API."""
    return who


admin = APIRouter(tags=["Admin"])
admin.include_router(user_router, prefix="/users")
admin.include_router(settings_router, prefix="/settings")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(admin, prefix="/admin")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

"""Main module for the API."""
import toml  # type: ignore
from fastapi import APIRouter, FastAPI, status

from api.auth.router import router as auth_router
from api.database import engine, init_db
from api.environment import db, env
from api.healthcheck.router import router as healthcheck_router
from api.myself.router import router as myself_router
from api.settings.router import router as settings_router
from api.settings.router import settings
from api.settings.utils import load, save
from api.users.router import router as user_router

# Get app name and version from pyproject.toml
app_name = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
website = toml.load("pyproject.toml")["tool"]["poetry"]["repository"]


# API Initialization parameters
start: dict[str, any] = {}  # type: ignore
start["title"] = app_name
start["version"] = app_version
start["description"] = "API for the " + app_name + " application."
start["debug"] = env.local.is_debug
start["license_info"] = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
start["contact"] = {"name": "Bruno Botelho", "url": website, "email": "bruno.botelho.br@gmail.com"}
if env.local.is_debug is True:
    start["redoc_url"] = "/redoc"
    start["openapi_url"] = "/openapi.json"
    start["docs_url"] = "/"
else:
    start["redoc_url"] = None
    start["openapi_url"] = None
    start["docs_url"] = None


# Create FastAPI instance
app = FastAPI(**start)


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
    engine.dispose()


# About Endpoints
@app.get("/version", tags=["About"], status_code=status.HTTP_200_OK)
def version() -> dict[str, str]:
    """Version endpoint for the API."""
    return {"version": app_version}


# Enpoints
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(myself_router, prefix="/myself", tags=["Myself"])
admin = APIRouter(tags=["Admin"])
admin.include_router(user_router, prefix="/users")
admin.include_router(settings_router, prefix="/settings")
app.include_router(admin, prefix="/admin")
app.include_router(healthcheck_router, prefix="/healthcheck", tags=["Healthcheck"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

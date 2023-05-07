"""Main module for the API."""
from fastapi import APIRouter, FastAPI

from api.about.router import router as about_router
from api.core.constants import app_start_parameters
from api.core.database import reset_database, shutdown_database
from api.core.environment import database_environment, running_environment
from api.core.healthcheck.router import router as healthcheck_router
from api.core.settings.router import router as settings_router

# from api.myself.router import router as myself_router
from api.users.router import router as user_router

# Create FastAPI instance
app = FastAPI(**app_start_parameters)


# On Startup event
@app.on_event("startup")
async def startup() -> None:
    """Triggered when the application is starting up."""
    # Check if the environment is initialized
    if running_environment is None:
        raise ValueError("EnvironmentBehavior not initialized")
    if database_environment is None:
        raise ValueError("Database settings not initialized")
    # Initialize database, if debug mode is enabled
    if running_environment.local.is_debug:
        if reset_database() is False:
            raise ValueError("Database reset failed")


# On Shutdown event
@app.on_event("shutdown")
async def shutdown() -> None:
    """Triggered when the application is shutting down."""
    shutdown_database()


# Assigning endpoints
app.include_router(prefix="/about", tags=["About"], router=about_router)
admin = APIRouter(tags=["Admin"])
admin.include_router(prefix="/users", router=user_router)
admin.include_router(prefix="/settings", router=settings_router)

app.include_router(prefix="/admin", router=admin)
app.include_router(prefix="/healthcheck", tags=["Healthcheck"], router=healthcheck_router)

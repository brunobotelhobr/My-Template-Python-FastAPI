"""Main module for the API."""
from fastapi import APIRouter, FastAPI

from api.about.router import router as about_router
from api.auth.router import router as auth_router
from api.core.constants import app_start_parameters
from api.core.database import engine, initialize_database
from api.core.environment import database_environment, running_environment
from api.healthcheck.router import router as healthcheck_router
from api.myself.router import router as myself_router
from api.settings.router import router as settings_router
from api.settings.utils import global_settings, load, save
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
        initialize_database()
    # initialize settings
    if load(global_settings) is False:
        save(global_settings)


# On Shutdown event
@app.on_event("shutdown")
async def shutdown() -> None:
    """Triggered when the application is shutting down."""
    engine.dispose()


# Assigning endpoints
app.include_router(about_router, prefix="/about", tags=["About"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(myself_router, prefix="/myself", tags=["Myself"])
admin = APIRouter(tags=["Admin"])
admin.include_router(user_router, prefix="/users")
admin.include_router(settings_router, prefix="/settings")
app.include_router(admin, prefix="/admin")
app.include_router(healthcheck_router, prefix="/healthcheck", tags=["Healthcheck"])

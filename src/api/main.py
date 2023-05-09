"""Main module for the API."""
from fastapi import APIRouter, FastAPI

from api.about.router import router as about_router
from api.auth.router import router as auth_router
from api.core.constants import app_start_parameters
from api.core.database import reset as reset_database
from api.core.database import shutdown as shutdown_database
from api.core.database import test as test_database
from api.core.healthcheck.router import router as healthcheck_router
from api.core.settings.router import router as settings_router
from api.core.utils import environment
from api.users.router import router as user_router

# Create FastAPI instance
app = FastAPI(**app_start_parameters)


# On Startup event
@app.on_event("startup")
async def startup() -> None:
    """Triggered when the application is starting up."""
    # Check if the environment is initialized
    if environment is None:
        raise ValueError("Environment not initialized")
    # Initialize the database, if debug
    if environment.behavior.is_debug:
        # Reset the database
        reset_database()
    # Test the database connection, raise error if not possible.
    if not test_database():
        raise ValueError("Database connection failed")
    # Finish Lazzy Loader
    environment.database_lazzy_loader = False


# On Shutdown event
@app.on_event("shutdown")
async def shutdown() -> None:
    """Triggered when the application is shutting down."""
    shutdown_database()


# Assigning endpoints
app.include_router(prefix="/about", tags=["About"], router=about_router)
app.include_router(prefix="/auth", tags=["Auth"], router=auth_router)
admin = APIRouter(tags=["Admin"])
admin.include_router(prefix="/users", router=user_router)
admin.include_router(prefix="/settings", router=settings_router)

app.include_router(prefix="/admin", router=admin)
app.include_router(prefix="/healthcheck", tags=["Healthcheck"], router=healthcheck_router)

# Run the application if the file is executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

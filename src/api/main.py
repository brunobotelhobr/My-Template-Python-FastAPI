"""Main module for the API."""
import toml  # type: ignore
from fastapi import FastAPI

from api.database import init_db
from api.environment import db, env
from api.settings.router import router as settings_router
from api.settings.router import settings
from api.users.router import router as user_router

app_name = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

app = FastAPI(
    title=app_name,
    version=app_version,
    debug=env.local.is_debug,
    docs_url="/",
)


@app.on_event("startup")
async def startup() -> None:
    """Triggered when the application is starting up."""
    print("Starting up...")
    # Check if the environment is initialized
    if env is None:
        raise ValueError("Enviroment not initialized")
    if db is None:
        raise ValueError("Database settings not initialized")
    if env.local.is_debug:
        print("Creating database tables...")
        init_db()
    print("Loading configuration...")
    settings.load()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Triggered when the application is shutting down."""
    print("Shutting down...")


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint for load balancers."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    """Version endpoint for the API."""
    return {"version": app_version}


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(settings_router, prefix="/admin/settings", tags=["Settings"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

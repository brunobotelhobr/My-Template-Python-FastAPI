from datetime import datetime

from fastapi import APIRouter, status
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from toml import load  # type: ignore

from api.database import engine
from api.healthcheck.schema import Entity, HealthCheck

router = APIRouter()


@router.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def healthcheck() -> HealthCheck:
    """Healthcheck endpoint for load balancers."""
    with Session(engine) as session:
        lstart = datetime.now()
        q = text("SELECT 1")
        session.execute(q)
        # Count Tables
        ispn = inspect(engine)
        t = 0
        for _ in ispn.get_table_names():
            t += 1
        d = {}
        d["flavor"] = engine.name
        d["dialect"] = engine.dialect.name
        d["driver"] = engine.driver
        d["host"] = str(engine.url.host)
        d["port"] = str(engine.url.port)
        d["database"] = str(engine.url.database)
        d["table count"] = str(t)

    dbe = Entity(alias="database", status="ok", timeTaken=str(datetime.now() - lstart), details=d)
    start = datetime.now()
    d: dict[str, str] = {}  # type: ignore
    d["name"] = load("pyproject.toml")["tool"]["poetry"]["name"]
    d["version"] = load("pyproject.toml")["tool"]["poetry"]["version"]
    return HealthCheck(status="ok", timeTaken=str(datetime.now() - start), details=d, entities=[dbe])

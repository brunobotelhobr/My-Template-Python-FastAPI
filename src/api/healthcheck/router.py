"""Healthcheck router."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from toml import load  # type: ignore

from api.auth.utils import authenticate
from api.database import engine
from api.healthcheck.schema import Entity, HealthCheck
from api.users.schema import UserOut

router = APIRouter()


@router.get("/", response_model=HealthCheck, status_code=status.HTTP_200_OK)
def simple_healthcheck() -> HealthCheck:
    """Do simple healthcheck endpoint for load balancers."""
    with Session(engine) as session:
        lstart = datetime.now()
        q = text("SELECT 1")
        session.execute(q)
    start = datetime.now()
    dbe = Entity(alias="database", status="ok", timeTaken=str(datetime.now() - lstart), details=None)
    return HealthCheck(status="ok", timeTaken=str(datetime.now() - start), details=None, entities=[dbe])


@router.get("/full", response_model=HealthCheck, status_code=status.HTTP_200_OK)
async def full_healthcheck(me: UserOut = Depends(authenticate)) -> HealthCheck:
    """Do complete healthcheck endpoint for load balancers."""
    # check if me is valid
    if me is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    with Session(engine) as session:
        lstart = datetime.now()
        q = text("SELECT 1")
        session.execute(q)
        # Count Tables
        ispn = inspect(engine)
        d: dict[str, str] = {}
        d["flavor"] = str(ispn.engine.name)
        d["dialect"] = str(ispn.engine.dialect.name)
        d["driver"] = str(ispn.engine.driver)
        d["host"] = str(ispn.engine.url.host)
        d["port"] = str(ispn.engine.url.port)
        d["database"] = str(ispn.engine.url.database)
        d["table count"] = str(len(ispn.get_table_names()))

    dbe = Entity(alias="database", status="ok", timeTaken=str(datetime.now() - lstart), details=d)
    start = datetime.now()
    d: dict[str, str] = {}  # type: ignore
    d["name"] = load("pyproject.toml")["tool"]["poetry"]["name"]
    d["version"] = load("pyproject.toml")["tool"]["poetry"]["version"]
    return HealthCheck(status="ok", timeTaken=str(datetime.now() - start), details=d, entities=[dbe])

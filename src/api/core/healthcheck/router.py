"""Healthcheck router."""
from datetime import datetime

import toml
from fastapi import APIRouter, status
from sqlalchemy import inspect
from sqlalchemy.sql import text

from api.core.database import engine, session
from api.core.healthcheck.schema import Entity, HealthCheck

router = APIRouter()


@router.get(
    "/",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Healthcheck"},
        500: {"description": "Internal Server Error"},
    },
)
def simple_healthcheck() -> HealthCheck:
    """
    Get Healthcheck.

    Do simple healthcheck endpoint for load balancers.
    """
    # Check Database
    with session() as dabase_session:
        lstart = datetime.now()
        database_query = text("SELECT 1")
        dabase_session.execute(database_query)
        # Count Tables
        ispn = inspect(engine)
        database_details: dict[str, str] = {}
        database_details["flavor"] = str(ispn.engine.name)
        database_details["dialect"] = str(ispn.engine.dialect.name)
        database_details["driver"] = str(ispn.engine.driver)
        database_details["table count"] = str(len(ispn.get_table_names()))
    # Create Entity
    dbe = Entity(
        alias="database",
        status="ok",
        timeTaken=str(datetime.now() - lstart),
        details=database_details,
    )

    # Consolidate
    start = datetime.now()
    api_details: dict[str, str] = {}  # type: ignore
    api_details["name"] = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
    api_details["version"] = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    # Adjust the status
    main_status = "ok"
    if dbe.status == "ok":
        main_status = "ok"

    # Response
    return HealthCheck(
        status=main_status,
        timeTaken=str(datetime.now() - start),
        details=api_details,
        entities=[dbe],
    )

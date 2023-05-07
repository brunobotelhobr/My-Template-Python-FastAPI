"""Paginator schema."""
from math import ceil
from typing import List

from fastapi import Query
from pydantic import BaseModel

from api.core.database import BaseModelORM, session
from api.core.settings.utils import get_running_settings


class QueryBase(BaseModel):
    """
    Common query parameters schema.

    This is a Base Model for Paginated Response.

    Args:
        page (int): Page number to return.
        records (int): Number of records to return.
    """

    page: int = Query(
        default=1, title="Page number", description="Page number to return.", gt=0
    )
    records: int = Query(
        default=100,
        title="Records per page",
        description="Number of records to return.",
        gt=0,
        le=get_running_settings().api.page_size_max,
    )


class PageBase(BaseModel):
    """
    Page Base Model.

    This is  a Base Model for Paginated Response.
    Args:
        records (List[Type[BaseModel]]): List of Pydantic Models.
        query (QueryBase): Pydantic Query Model, herated from QueryBase.
        total_pages (int): Total pages.
        total_records (int): Total records.
    """

    records: List[BaseModel]
    query: QueryBase
    total_pages: int
    total_records: int


def executor(orm, schema: BaseModel, query: QueryBase) -> PageBase:
    """
    Do SQL Alchmy queries, and return a page with the results.

    Args:
        orm (BaseModelORM): An Registred SQL Alchemy ORM Model.
        schema (BaseModel): Pydantic Schema Model.
        query (QueryBase): Pydantic Query Model, herated from QueryBase.

    Raises:
        ValueError: If orm_model is unknown.

    Returns:
        PageBase: Pydantic Page Model.
    """
    # validate if the orm_model is known.
    if orm not in BaseModelORM.__subclasses__():
        raise ValueError(f"orm model {orm} is unknown.")
    # Run Query
    with session() as database:
        total_records = database.query(orm).count()
        total_pages = ceil(total_records / query.records)
        records_database = (
            database.query(orm).offset(query.page - 1).limit(query.records).all()
        )
        # Convert to Pydantic Model
        records: List[BaseModel] = []
        for record in records_database:
            records.append(schema.from_orm(record))
        # Return Page
        return PageBase(
            records=records,  # type: ignore
            query=query,
            total_pages=total_pages,
            total_records=total_records,
        )

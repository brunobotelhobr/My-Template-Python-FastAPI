"""Paginator Utils."""
from math import ceil
from typing import List

from pydantic import BaseModel

from api.core.database import BaseModelORM, session
from api.core.paginator.model import PageBase, QueryBase


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
    with session() as database_session:
        total_records = database_session.query(orm).count()
        total_pages = ceil(total_records / query.records)
        records_database = database_session.query(orm).offset(query.page - 1).limit(query.records).all()
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

"""Paginator schema."""
from typing import List

from fastapi import Query
from pydantic import BaseModel

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

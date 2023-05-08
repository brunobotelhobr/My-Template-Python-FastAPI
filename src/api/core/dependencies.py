"""General API dependencies."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from api.core.database import get_database_session
from api.core.paginator.model import QueryBase
from api.core.settings.model import RunningSettings
from api.core.settings.utils import get_running_settings
from api.core.utils import HashHandler, RandomGenerator, get_generator, get_hash_handler

# API Dependencies
Database = Annotated[Session, Depends(get_database_session)]
Settings = Annotated[RunningSettings, Depends(get_running_settings)]
QueryParameters = Annotated[QueryBase, Depends()]
HashManager = Annotated[HashHandler, Depends(get_hash_handler)]
Generator = Annotated[RandomGenerator, Depends(get_generator)]

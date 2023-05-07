"""General API dependencies."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from api.core.database import get_database_session
from api.core.paginator.schema import QueryBase
from api.core.settings.schema import RunningSettings
from api.core.settings.utils import get_running_settings
from api.core.utils import HashHandler, RandomGenerator

Database = Annotated[Session, Depends(get_database_session)]
Settings = Annotated[RunningSettings, Depends(get_running_settings)]
QueryParameters = Annotated[QueryBase, Depends()]
HashManager = Annotated[HashHandler, Depends()]
Generator = Annotated[RandomGenerator, Depends()]

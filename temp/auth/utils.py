"""Auth Model."""
# from datetime import datetime, timedelta

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# from api.core.jwt.orm import RevokedTokenORM
# from api.auth.model import RevokedToken
# from api.core.database import get_database_session
# from api.core.dependencies import Settings
# from api.users.model import UserORM
# from api.users.schema import UserOut

# bad_tokens = []


# def authenticate(
#     token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
#     database: Session = Depends(get_database_session),
# ) -> UserOut:
#     """Authenticate user."""
#     email = jwt_factory.verify(token)
#     q = database.query(UserORM).filter(UserORM.email == email).first()
#     if not q:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Bad credentials.",
#         )
#     u = UserOut(**q.__dict__)  # type: ignore
#     if u.blocked:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: User is blocked.",
#         )
#     return u


# jwt_factory = JWTFactory()

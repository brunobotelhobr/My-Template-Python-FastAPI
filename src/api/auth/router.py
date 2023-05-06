"""Authentication Router."""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from api.auth.schema import AuthRequest, Token
from api.auth.utils import authenticate, jwt_factory  # type: ignore
from api.core.database import get_database_session
from api.core.dependencies import Database
from api.core.schema import SimpleMessage
from api.core.utils import hash_handler
from api.settings.router import global_settings
from api.users.model import UserORM
from api.users.schema import UserDB, UserOut

router = APIRouter()


# @router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
# def login(
#     form: OAuth2PasswordRequestFormStrict = Depends(),
#     database: Database,
# ):
#     """Check if user exists and return JWT."""
#     # Validate Received Data
#     try:
#         credetials = AuthRequest(email=form.username, password=form.password)  # type: ignore
#     except ValueError as error:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Bad request: Invalid credentials.",
#         ) from error
#     # User Exists?
#     user_db_query = (
#         database.query(UserORM).filter(UserORM.email == credetials.username).first()
#     )
#     if not user_db_query:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Bad credentials.",
#         )
#     # Password is correct?
#     user_db = UserDB(**user_db_query.__dict__)  # type: ignore
#     if (
#         hash_handler.verify_hash(password=credetials.password, hash=user_db.password_hash)
#         is False
#     ):
#         # Update password attempts count.
#         user_db_query.password_strikes += 1  # type: ignore
#         if global_settings.auth.block_user_after_fail_attempts > 0:
#             if (
#                 user_db_query.password_strikes
#                 >= global_settings.auth.block_user_after_fail_attempts
#             ):
#                 user_db_query.blocked = True  # type: ignore
#         database.add(user_db_query)
#         database.commit()
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Bad credentials.",
#         )
#     # User is blocked?
#     if user_db.blocked:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: User is blocked.",
#         )
#     # Reset password attempts count.
#     if user_db.password_strikes > 0:
#         user_db_query.password_strikes = 0  # type: ignore
#         database.add(user_db_query)
#         database.commit()
#     # Generate JWT.
#     t = jwt_factory.create(user_db.email)
#     return {"token_type": "bearer", "access_token": t}


@router.get("/renew", status_code=status.HTTP_200_OK, response_model=Token)
def renew(req: Request, who: UserOut = Depends(authenticate)):
    """Renew JWT."""
    # check if me is valid
    if who is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized: Invalid credentials.",
        )
    jwt_factory.revoke(req.headers["authorization"])
    token = jwt_factory.renew(req.headers["authorization"])
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized: Invalid credentials.",
        )
    return {"token_type": "bearer", "access_token": token}


@router.get("/logout", status_code=status.HTTP_302_FOUND)
def logout(req: Request, who: UserOut = Depends(authenticate)) -> JSONResponse:
    """Logout endpoint for the API."""
    if who is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized: Bad credentials.",
        )
    if req.cookies.get("Authorization"):
        jwt_factory.revoke(req.cookies["Authorization"])
    if req.headers.get("Authorization"):
        jwt_factory.revoke(req.headers["Authorization"])
    resp = JSONResponse(
        content=SimpleMessage(status="Sucessfully logged out.").json(),
        status_code=status.HTTP_302_FOUND,
    )
    resp.delete_cookie("Authorization")
    resp.headers["Authorization"] = ""
    return resp

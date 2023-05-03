"""Authentication Router."""
from time import process_time_ns
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.auth.schema import AuthRequest, Token
from api.auth.utils import authenticate, jwt_factory  # type: ignore
from api.database import get_db
from api.schema import SimpleMessage
from api.settings.router import global_settings
from api.users.model import UserORM
from api.users.schema import UserDB, UserOut
from api.utils import generator

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    """Check if user exists and return JWT."""
    try:
        credetials = AuthRequest(email=form.username, password=form.password)  # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request: Invalid credentials.") from e
    # User Exists?
    q = database.query(UserORM).filter(UserORM.email == credetials.email).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    # Password is correct?
    u = UserDB(**q.__dict__)  # type: ignore
    if u.password_hash != generator.hasher(password=credetials.password, salt=u.salt):
        # Update password attempts count.
        q.password_attempts_count += 1  # type: ignore
        if global_settings.auth.block_user_after_fail_attempts > 0:
            if q.password_strikes >= global_settings.auth.block_user_after_fail_attempts:
                q.blocked = True  # type: ignore
        database.add(q)
        database.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    # User is blocked?
    if u.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: User is blocked.")
    # Reset password attempts count.
    if u.password_strikes > 0:
        q.password_strikes = 0  # type: ignore
        database.add(q)
        database.commit()
    # Generate JWT.
    t = jwt_factory.create(u.email)
    return {"token_type": "bearer", "access_token": t}


@router.get("/renew", status_code=status.HTTP_200_OK, response_model=Token)
def renew(req: Request, me: UserOut = Depends(authenticate)):
    """Renew JWT."""
    # check if me is valid
    t = jwt_factory.renew(req.headers["authorization"])
    if t is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Invalid credentials.")
    return {"token_type": "bearer", "access_token": t}


@router.get("/logout", status_code=status.HTTP_302_FOUND)
def protected_route(req: Request, me: UserOut = Depends(authenticate)) -> JSONResponse:
    """Logout endpoint for the API."""
    if me is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    if req.cookies.get("Authorization"):
        jwt_factory.revoke(req.cookies["Authorization"])
    if req.headers.get("Authorization"):
        jwt_factory.revoke(req.headers["Authorization"])
    resp = JSONResponse(content=SimpleMessage(status="Sucessfully logged out.").json(), status_code=status.HTTP_302_FOUND)
    resp.delete_cookie("Authorization")
    resp.headers["Authorization"] = ""
    return resp

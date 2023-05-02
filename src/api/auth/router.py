from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.auth.schema import AuthRequest, Token
from api.auth.utils import jwt_factory
from api.database import session
from api.settings.router import settings
from api.users.model import UserORM
from api.users.schema import UserDB, UserOut
from api.utils import generator

router = APIRouter()
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Dependency
def get_db():
    """Dependency to get a database session."""
    database = session()
    try:
        yield database
    finally:
        database.close()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    """Check if user exists and return JWT."""
    try:
        credetials = AuthRequest(email=form.username, password=form.password)  # type: ignore
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request: Invalid credentials.")
    q = database.query(UserORM).filter(UserORM.email == credetials.email).first()
    # User Exists?
    if not q:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    # Password is correct?
    u = UserDB(**q.__dict__)  # type: ignore
    print(u.__dict__)
    if u.password_hash != generator.hasher(password=credetials.password, salt=u.salt):
        # Update password attempts count.
        q.password_attempts_count += 1  # type: ignore
        if settings.auth.block_user_after_fail_attempts > 0:
            if q.password_attempts_count >= settings.auth.block_user_after_fail_attempts:
                q.blocked = True  # type: ignore
        database.add(q)
        database.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    # User is blocked?
    if u.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: User is blocked.")
    # Reset password attempts count.
    if u.password_attempts_count > 0:
        q.password_attempts_count = 0  # type: ignore
        database.add(q)
        database.commit()
    # Generate JWT.
    t = jwt_factory.create(u.email)
    return {"token_type": "bearer", "access_token": t}


def authenticate(token: str = Depends(oauth_schema), database: Session = Depends(get_db)) -> UserOut:
    """Authenticate user."""
    email = jwt_factory.verify(token)
    q = database.query(UserORM).filter(UserORM.email == email).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
    u = UserOut(**q.__dict__)  # type: ignore
    if u.blocked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: User is blocked.")
    return u

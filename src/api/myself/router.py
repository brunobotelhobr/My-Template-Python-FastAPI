from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.utils import authenticate
from api.database import get_db
from api.myself.schema import PasswordResetRequest
from api.users.model import UserORM
from api.users.schema import UserDB, UserIn, UserOut
from api.utils import generator

router = APIRouter()


@router.get("/", response_model=UserOut)
def myself(me: UserOut = Depends(authenticate)) -> UserOut:
    """Me endpoint for the API."""
    return me


@router.post("/password-reset", status_code=status.HTTP_200_OK)
def password_reset(p: PasswordResetRequest, me: UserOut = Depends(authenticate), database: Session = Depends(get_db)):
    """Password reset endpoint for the API."""
    if p.new == p.confirm:
        with database as session:
            q = session.query(UserORM).filter(UserORM.email == me.email).first()
            u = UserDB(**q.__dict__)
            new_hash = generator.hasher(password=p.new, salt=u.salt)
            if new_hash == u.password_hash:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="New password cannot be the same as the old one.")
            try:
                _ = UserIn(email=u.email, name=u.name, password=p.new)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Bad request: Invalid password.") from e
            hash = generator.hasher(password=p.new, salt=u.salt)
            u.password_hash = hash
            u.password_setting_date = generator.now()
            for k, v in u.__dict__.items():
                setattr(q, k, v)
            session.add(q)
            session.commit()
            return {"status": "sucessfully changed password"}

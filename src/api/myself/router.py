"""Myself router."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.auth.utils import authenticate
from api.database import get_db
from api.myself.schema import PasswordResetRequest
from api.schema import SimpleMessage
from api.settings.utils import global_settings
from api.users.model import UserORM
from api.users.schema import UserDB, UserOut
from api.utils import generator

router = APIRouter()


@router.get("/", response_model=UserOut)
def myself(me: UserOut = Depends(authenticate)) -> UserOut:
    """Me endpoint for the API."""
    return me


@router.post("/password-reset", status_code=status.HTTP_200_OK, response_model=SimpleMessage)
def password_reset(p: PasswordResetRequest, me: UserOut = Depends(authenticate), database: Session = Depends(get_db)):
    """Password reset endpoint for the API."""
    # Check if the new password and confirm password are the same
    if p.new.password != p.confirm.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="New password and confirm password do not match.")

    with database as session:
        q = session.query(UserORM).filter(UserORM.email == me.email).first()
        u = UserDB(**q.__dict__)
        # Check if the old password is correct
        old_hash = generator.hasher(password=p.old, salt=u.salt)
        if old_hash != u.password_hash:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized: Bad credentials.")
        # Generate new password hash
        new_hash = generator.hasher(password=p.new.password, salt=u.salt)
        # Check if the new password is the same as the old one
        if global_settings.users.allow_password_reset:
            if new_hash == old_hash:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="New password cannot be the same as the old one.")
        # Update password hash and birthday
        u.password_hash = new_hash
        u.password_birthday = generator.now()
        for k, v in u.__dict__.items():
            setattr(q, k, v)
        session.add(q)
        session.commit()
        return SimpleMessage(status="Password updated successfully.")

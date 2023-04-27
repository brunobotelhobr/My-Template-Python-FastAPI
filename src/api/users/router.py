"""User router."""
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.config import configuration
from api.database import engine, session
from api.users import crud, model, schema
from api.utils import generator

router = APIRouter()

# Create database tables.
model.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """Dependency to get a database session."""
    db = session()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schema.UserOut], status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """Get all users."""
    out = crud.user_list(database=database, skip=skip, limit=limit)
    return out


@router.post("/", response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schema.UserIn, database: Session = Depends(get_db)):
    """Create a new user."""
    key = generator.get_uuid()
    while crud.user_get_by(database=database, attribute="key", value=key) is not None:
        key = generator.get_uuid()
    salt = schema.generator.get_salt()
    hassed_password = generator.get_password_hash(password=user_in.password, salt=salt)
    user_db = schema.UserDB(**user_in.dict(), salt=salt, hashed_password=hassed_password, key=key)
    return crud.user_save(database=database, user=(model.UserORM(**user_db.dict())))


@router.get("/{key}}", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def get_user(key: str, database: Session = Depends(get_db)):
    """Get a user."""
    user = crud.user_get_by(database=database, attribute="key", value=key)
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{key}", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def delete_user(key: str, database: Session = Depends(get_db)):
    """Delete a user."""
    if configuration.users.allow_delete is False:
        raise HTTPException(status_code=404, detail="Delete is not allowed in this environment")
    if crud.user_get_by(database=database, attribute="key", value=key) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.user_delete(database=database, key=key)


@router.patch("/{key}", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def update_user(key: str, user: schema.UserBase, database: Session = Depends(get_db)):
    """Update a user."""
    # Check if user exists
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if email is already registered for another user
    if user.email != user_db.email:
        if crud.user_get_by(database=database, attribute="email", value=user.email):
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

    return crud.user_update(database=database, user=user_db, update_dict=user.dict())


@router.get("/{key}}/verifify", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def verify_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Verify a user."""
    # Check if user exists
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_verified": True})


@router.get("/{key}}/deverifify", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def deverify_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Deverify a user."""
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_verified": False})


@router.get("/{key}}/activate", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def activate_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Activate a user."""
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_active": True})


@router.get("/{key}}/deactivate", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def deactivate_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Deactivate a user."""
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_active": False})


@router.get("/{key}/block", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def block_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Block a user."""
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_blocked": True})


@router.get("/{key}/unblock", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def unblock_user(key: str, database: Session = Depends(get_db)) -> schema.UserOut:
    """Unblock a user."""
    user_db = crud.user_get_by(database=database, attribute="key", value=key)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_update(database=database, user=user_db, update_dict={"is_blocked": False})


@router.post("/{key}/reset_my_password", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def reset_my_password(
    key: str,
    new_password: str = Body(..., example="NewP@ssw0rd"),
    actual_password: str = Body(..., example="ActualP@ssw0rd"),
    database: Session = Depends(get_db),
):
    """Reset a user password."""

    # Check if user exists
    db_user = crud.user_get_by(database=database, attribute="key", value=key)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if new password is equal to old password
    if new_password == actual_password:
        raise HTTPException(
            status_code=400,
            detail="New password is equal to old password",
        )

    # Check if the password meet complexity requirements
    fake_name = generator.get_key()
    fake_email = generator.get_key() + "@example.com"
    try:
        schema.UserIn(name=fake_name, email=fake_email, password=new_password)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Password does not meet complexity requirements",
        )

    new_password = schema.userutils.salt_password(password=new_password, salt=db_user.salt)
    actual_password = schema.userutils.salt_password(password=actual_password, salt=db_user.salt)
    if configuration.USERS_PASSWORD_ALLOW_REUSE is False:
        # Check if new password is to the database user password
        if db_user.hashed_password == new_password:
            raise HTTPException(
                status_code=400,
                detail="New password is equal to old password",
            )
    if actual_password != db_user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Actual password is not correct.",
        )
    return crud.user_update(
        database=database, user=db_user, update_dict={"hashed_password": new_password, "salt": db_user.salt}
    )


@router.post("/{key}/reset_password", response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def reset_password(key: str, new_password: str = Body(..., example="NewP@ssw0rd"), database: Session = Depends(get_db)):
    """Reset a user password."""
    db_user = crud.user_get_by(database=database, attribute="key", value=key)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the password meet complexity requirements
    fake_name = generator.get_key()
    fake_email = generator.get_key() + "@example.com"
    try:
        schema.UserIn(name=fake_name, email=fake_email, password=new_password)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Password does not meet complexity requirements",
        )

    new_password = schema.userutils.salt_password(password=new_password, salt=db_user.salt)
    return crud.user_update(
        database=database, user=db_user, update_dict={"hashed_password": new_password, "salt": db_user.salt}
    )

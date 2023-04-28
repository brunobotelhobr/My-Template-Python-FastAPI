from fastapi import APIRouter, Depends, HTTPException, status

from api.auth.model import AuthRequest, JWTFactory, UserDB

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(user: AuthRequest):
    """Login route."""

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return {"access_token": auth.jwt.generate(user)}

"""Auth Router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.core.jwt.model import AuthForm, AuthRequest, Token
from api.core.jwt.utils import authenticate, barear, renew, revoke
from api.core.model import SimpleMessage

router = APIRouter()


@router.post(
    "/login-form",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        200: {"description": "Successful Response."},
        400: {"description": "Bad Request: Invalid credentials."},
        403: {"description": "Forbidden: Wrong credetials or user is not active, not verified or is blocked."},
        500: {"description": "Internal Server Error."},
    },
)
def post_login_form(form: AuthForm = Depends()) -> Token:
    """
    Post Login Form.

    Will return a JWT token if the user credentials are valid and the user is:
    - Verified
    - Active
    - Not Blocked
    """
    # Validate Received Data
    try:
        credentials = AuthRequest(username=form.username, password=form.password)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request: Invalid credentials.",
        ) from error
    return authenticate(credentials=credentials)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        200: {"description": "Successful Response."},
        400: {"description": "Bad Request: Invalid credentials."},
        403: {"description": "Forbidden: Wrong credetials or user is not active, not verified or is blocked."},
        500: {"description": "Internal Server Error."},
    },
)
def post_login(credentials: AuthRequest) -> Token:
    """
    Post Login.

    Will return a JWT token if the user credentials are valid and the user is:
    - Verified
    - Active
    - Not Blocked
    """
    return authenticate(credentials=credentials)


@router.get("/validate", status_code=status.HTTP_200_OK, response_model=SimpleMessage)
def get_validate(token: Annotated[str, Depends(barear)]):
    """Get Validate."""
    if token:
        return SimpleMessage(status="Token is valid.")


@router.get("/renew", status_code=status.HTTP_200_OK, response_model=Token)
def get_renew(token: Annotated[str, Depends(barear)]):
    """Get Renew."""
    new_token = renew(token=Token(access_token=token))
    revoke(token=Token(access_token=token))
    return new_token


@router.get("/logout", status_code=status.HTTP_200_OK, response_model=SimpleMessage)
def get_logout(token: Annotated[str, Depends(barear)]):
    """Get Logout."""
    revoke(token=Token(access_token=token))
    return SimpleMessage(status="Logout successful.")

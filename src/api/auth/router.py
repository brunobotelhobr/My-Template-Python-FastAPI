"""Auth Router."""
from fastapi import APIRouter, Depends, HTTPException, status

from api.core.jwt.model import AuthForm, AuthRequest, Token
from api.core.jwt.utils import authenticate

router = APIRouter()


@router.post("/login-form", status_code=status.HTTP_200_OK, response_model=Token)
def post_login_form(form: AuthForm = Depends()) -> Token:
    """
    Post Login.

    Will return a JWT token if the user credentials are valid.

    Args:
        form (AuthForm): Form with username and password.

    Returns:
        Token: JWT token.
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


# @router.get("/renew", status_code=status.HTTP_200_OK, response_model=Token)
# def renew(req: Request, who: UserOut = Depends(authenticate)):
#     """Renew JWT."""
#     # check if me is valid
#     if who is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Invalid credentials.",
#         )
#     jwt_factory.revoke(req.headers["authorization"])
#     token = jwt_factory.renew(req.headers["authorization"])
#     if token is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Invalid credentials.",
#         )
#     return {"token_type": "bearer", "access_token": token}


# @router.get("/logout", status_code=status.HTTP_302_FOUND)
# def logout(req: Request, who: UserOut = Depends(authenticate)) -> JSONResponse:
#     """Logout endpoint for the API."""
#     if who is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authorized: Bad credentials.",
#         )
#     if req.cookies.get("Authorization"):
#         jwt_factory.revoke(req.cookies["Authorization"])
#     if req.headers.get("Authorization"):
#         jwt_factory.revoke(req.headers["Authorization"])
#     resp = JSONResponse(
#         content=SimpleMessage(status="Sucessfully logged out.").json(),
#         status_code=status.HTTP_302_FOUND,
#     )
#     resp.delete_cookie("Authorization")
#     resp.headers["Authorization"] = ""
#     return resp


# @router.get("/validate", status_code=status.HTTP_200_OK, response_model=UserOut)

# """Myself router."""
# from fastapi import APIRouter, HTTPException, status

# from api.core.dependencies import Authenticate, Database, Generator, HashManager, Settings
# from api.core.schema import SimpleMessage
# from api.myself.schema import PasswordResetRequest
# from api.users.model import UserORM
# from api.users.schema import UserDB, UserOut

# router = APIRouter()


# @router.get("/", response_model=UserOut)
# def myself(who=Authenticate) -> UserOut:
#     """Me endpoint for the API."""
#     return who


# @router.post(
#     "/password-reset", status_code=status.HTTP_200_OK, response_model=SimpleMessage
# )
# def password_reset(
#     password_requet: PasswordResetRequest,
#     who=Authenticate,
#     database=Database,
#     settings=Settings,
#     hash_handler=HashManager,
#     generator=Generator,
# ):
#     """Password reset endpoint for the API."""
#     with database as session:
#         user_db_query = session.query(UserORM).filter(UserORM.email == who.email).first()
#         user_db = UserDB(**user_db_query.__dict__)
#         # Check if the old password is correct
#         if (
#             hash_handler.verify_hash(
#                 password=password_requet.password, hash=user_db.password_hash
#             )
#             is False
#         ):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not authorized: Bad credentials.",
#             )
#         # Check if the new password is the same as the old one
#         if settings.users.allow_password_reset:
#             if hash_handler.verify_hash(
#                 password=password_requet.password_new, hash=user_db.password_hash
#             ):
#                 raise HTTPException(
#                     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                     detail="New password cannot be the same as the old one.",
#                 )
#         # Update password hash and birthday
#         user_db_query.password_hash = hash_handler.generate_hash(password=password_requet.password_new)  # type: ignore
#         user_db_query.password_birthday = generator.now()  # type: ignore
#         session.add(user_db_query)
#         session.commit()
#         return SimpleMessage(status="Password updated successfully.")

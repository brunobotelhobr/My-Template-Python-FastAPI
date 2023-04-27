"""User schema."""
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class UserBase(BaseModel):
    """User model."""

    name: str = Field(example="John Doe", title="Full name",
                      max_length=250, min_length=5)
    email: EmailStr = Field(example="john.doe@email.com", title="Email")

    @validator("name")
    def name_must_contain_space(cls, v):   # pylint: disable=E0213
        """Validate name must contain a space."""
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserIn(UserBase):
    """User input model."""

    password: SecretStr = Field(
        example="P@ssw0rd", title="Password", min_length=8, max_length=128)

    @validator("password")
    def passwords_match(cls, v):  # pylint: disable=E0213
        """Validate password and confirm_password match."""
        if len(v) < 8:
            raise ValueError("must be at least 8 characters")
        if len(v) > 128:
            raise ValueError("must be less than 128 characters")
        return v

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserOut(UserBase):
    """User output model."""

    class Config:
        """Set orm_mode to True to allow returning ORM objects."""

        orm_mode = True


class UserDB(UserBase):
    """User database model."""

    salt: SecretStr = Field(
        example="12345678", title="Salt", max_length=8, min_length=8)
    password_hash: SecretStr = Field(
        example="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", title="Password Hash"
    )

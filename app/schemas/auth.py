import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password mush have capital letters")

        if not re.search(r"[0-9]", value):
            raise ValueError("password must contain atleast one number")
        if not re.search(r"[!@#$%&*]", value):
            raise ValueError(
                "Password must contains one of these symbols [!,@,#,$,%,^,&,*]"
            )
        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=50)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)

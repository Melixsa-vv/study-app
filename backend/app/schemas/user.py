from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, AfterValidator
import re
from typing import Annotated

class UserBase(BaseModel):
    email: EmailStr
    user_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique user's name"
    )

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Public alias, not necesarily unique"
    )


def validate_password_complexity(value:str) -> str:
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase")
    
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase")
    
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one number")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValueError("Password must contain at least one special character")
    
    return value

PasswordStr = Annotated[
    str,
    Field(
        min_length=8,
        max_length=50
    ),
    AfterValidator(validate_password_complexity)
    
]

class UserCreate(UserBase):
    password: PasswordStr


class UserRead(UserBase):
    id: int
    created_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    user_name: str | None = Field(
        None,
        min_length=3,
        max_length=50
    )
    name: str | None = Field(
        None, 
        min_length=3,
        max_length=50
    )
    password: PasswordStr | None = None


    
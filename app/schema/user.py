from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    admin = "admin"
    client = "client"
    staff = "staff"


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    number: Optional[str] = None
    address: Optional[str] = None
    user_role: UserRole
    is_active: Optional[bool] = None


class CreateUserInput(User):
    hashed_password: str


class UserOutput(User):
    id: int
    model_config = {"from_attributes": True}


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class LoginOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    client = "client"
    staff = "staff"


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_id: str
    email: EmailStr
    user_role: UserRole
    is_active: bool


class CreateUserInput(User):
    password_hash: str

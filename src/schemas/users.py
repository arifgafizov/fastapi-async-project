from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from db.models.enums import Role


class UserBase(BaseModel):
    email: EmailStr
    role: Role


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

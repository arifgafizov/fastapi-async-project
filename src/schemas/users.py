from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from db.models.enums import Role


class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    role: Role


class UserCreate(UserBase):
    password: str
    profile: ProfileCreate


class User(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ProfileOut(ProfileCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserOut(User):
    profile: ProfileOut = None


class UserUpdate(UserBase):
    profile: ProfileCreate

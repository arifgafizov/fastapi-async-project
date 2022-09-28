from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh: str


class AuthUser(BaseModel):
    email: EmailStr
    password: str

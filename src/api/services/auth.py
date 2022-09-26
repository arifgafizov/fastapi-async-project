from datetime import datetime, timedelta
import json

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from jose import jwt, JWTError
from starlette import status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.settings import settings
from schemas.auth import Token
from schemas.users import User
from db.models import users
from db.setup import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_access_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, raw_password: str, hash_password: str) -> bool:
        return bcrypt.verify(raw_password, hash_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def create_access_token(cls, user: users.User) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_access_expiration),
            'sub': str(user_data.id),
            'user': user_data.json(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    @classmethod
    def validate_access_token(cls, token: str) -> User:
        exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exceptions from None
        user_data = json.loads(payload.get('user'))
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exceptions from None
        else:
            return user

    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

        query = select(users.User).where(users.User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise exception
        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_access_token(user)


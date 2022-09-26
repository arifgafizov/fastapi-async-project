from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder

from api.services.auth import AuthService
from db.models.users import User
from db.setup import get_session
from schemas.users import UserCreate, UserBase


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    def validate_user(self, user: User):
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

    async def validate_user_email(self, email: str):
        user = await self._get_user_from_email(email)
        if user:
            raise HTTPException(status_code=400, detail="User with such email already exists")

    async def _get(self, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_user_from_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self):
        result = await self.db.execute(select(User).order_by(User.id))
        return result.scalars().all()

    async def get_user(self, user_id: int):
        user = await self._get(user_id)
        self.validate_user(user)
        return user

    async def create_user(self, user: UserCreate):
        await self.validate_user_email(user.email)
        AuthService.hash_password(user.password)
        new_user = User(email=user.email,
                        role=user.role,
                        password_hash=AuthService.hash_password(user.password),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                        )
        self.db.add(new_user)
        await self.db.flush()
        return new_user

    async def update_user(self, user_id: int, user: UserBase):
        db_user = await self._get(user_id)
        self.validate_user(db_user)
        q = update(User).where(User.id == user_id)
        q = q.values(email=user.email)
        q = q.values(role=user.role)
        q.execution_options(synchronize_session="fetch")
        await self.db.execute(q)
        return jsonable_encoder(db_user)

    async def delete_user(self, user_id: int):
        user = await self._get(user_id)
        self.validate_user(user)
        return await self.db.delete(user)

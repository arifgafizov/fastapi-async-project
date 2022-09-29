from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from api.services.auth import AuthService
from db.models.users import User, Profile
from db.setup import get_session
from schemas.users import UserCreate, UserUpdate, ProfileCreate


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
        query = select(User).where(User.id == user_id).options(joinedload(User.profile))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_user_from_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self):
        result = await self.db.execute(select(User).order_by(User.id).options(joinedload(User.profile)))
        return result.scalars().all()

    async def get_user(self, user_id: int):
        user = await self._get(user_id)
        self.validate_user(user)
        return user

    async def create_user(self, user: UserCreate):
        await self.validate_user_email(user.email)
        new_user = User(email=user.email,
                        role=user.role,
                        password_hash=AuthService.hash_password(user.password),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                        )
        self.db.add(new_user)
        await self.db.flush()
        await self._create_profile(ProfileCreate(
            first_name=user.profile.first_name,
            last_name=user.profile.last_name,
            bio=user.profile.bio,
            is_active=user.profile.is_active
        ), new_user.id)
        return await self._get(new_user.id)

    async def update_user(self, user_id: int, user: UserUpdate):
        db_user = await self._get(user_id)
        self.validate_user(db_user)
        q_user = update(User).where(User.id == user_id)
        q_user = q_user.values(email=user.email)
        q_user = q_user.values(role=user.role)
        # q_user.execution_options(synchronize_session="fetch")

        q_profile = update(Profile).where(Profile.id == db_user.profile.id)
        q_profile = q_profile.values(first_name=user.profile.first_name)
        q_profile = q_profile.values(last_name=user.profile.last_name)
        q_profile = q_profile.values(bio=user.profile.bio)
        q_profile = q_profile.values(is_active=user.profile.is_active)

        await self.db.execute(q_user)
        await self.db.execute(q_profile)
        return jsonable_encoder(db_user)

    async def delete_user(self, user_id: int):
        user = await self._get(user_id)
        self.validate_user(user)
        return await self.db.delete(user)

    async def _create_profile(self, profile: ProfileCreate, user_id: int) -> Profile:
        new_profile = Profile(
            first_name=profile.first_name,
            last_name=profile.last_name,
            bio=profile.bio,
            is_active=profile.is_active,
            users_id=user_id
        )
        self.db.add(new_profile)
        await self.db.flush()
        return new_profile

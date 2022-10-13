import anyio
import pytest
from httpx import AsyncClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database

from api.services.auth import AuthService
from db.models.enums import Role
from db.models.users import User, users, profiles
from db.setup import get_session, Base
from main import app
from core.settings import settings


# test async db and url
SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
database = Database(SQLALCHEMY_TEST_DATABASE_URL)

# test async engine and session
a_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
Session = sessionmaker(a_engine, class_=AsyncSession, expire_on_commit=False)


# fixture that init_db run with tests
@pytest.fixture
def anyio_backend():
    return 'asyncio'


init_user = {
    "email": "test@example.com",
    "role": Role.teacher,
    "password_hash": AuthService.hash_password('supertest'),
}

init_profile = {
    "first_name": "test_name",
    "last_name": "test_surname",
    "bio": None,
    "is_active": True,
}


# auto clean up database before tests and add init user
async def init_db():
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(users.insert(), [init_user])
    async with a_engine.connect() as conn:
        result = await conn.execute(select(User).where(User.email == "test@example.com"))
        user = result.fetchone()
        await conn.execute(profiles.insert(), [{**init_profile, "users_id": user.id}])

# run asynchronous function init_db
anyio.run(init_db)


# get test db session function
async def get_test_session() -> Session:
    async with Session() as db:
        yield db
        await db.commit()

# overriding test db session for test app
app.dependency_overrides[get_session] = get_test_session


# async client for tests
@pytest.fixture
async def app_client():
    async with AsyncClient(app=app, base_url=f"http://{settings.server_host}:{settings.server_port}") as client:
        yield client

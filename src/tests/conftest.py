import anyio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database

from db.setup import get_session, Base
from main import app


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


# auto clean up database before tests
async def init_db():
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# run asynchronous function init_db
anyio.run(init_db)


# get test db session function
async def get_test_session() -> Session:
    async with Session() as db:
        yield db
        await db.commit()

# overriding test db session for test app
app.dependency_overrides[get_session] = get_test_session

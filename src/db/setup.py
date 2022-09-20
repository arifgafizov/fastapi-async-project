from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database

from core.settings import settings

Base = declarative_base()
database = Database(settings.database_url)
#
# engine = create_engine(
#     'postgresql+psycopg2://lms_user:superpassword@db/lms_db', future=True
# )
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
engine = create_async_engine(settings.database_url, echo=True, future=True)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> Session:
    async with Session() as db:
        yield db
        await db.commit()


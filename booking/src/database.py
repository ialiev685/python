from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL)
test_engine = create_async_engine(settings.DB_URL, poolclass=NullPool)
async_session_marker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

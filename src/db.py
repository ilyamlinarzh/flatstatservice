from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_ASYNCPG_URL,
        echo=True,
        pool_size=15,
        max_overflow=15
    )


def create_session_maker() -> async_sessionmaker[AsyncSession]:
    async_engine = create_engine()

    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )


async def get_async_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


class Base(DeclarativeBase):
    ...

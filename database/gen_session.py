from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_IP, POSTGRES_PORT, POSTGRES_DB


DATABASE_URL = (f"postgresql+asyncpg://"
                f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                f"{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DB}")
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autocommit=False,
    autoflush=False, class_=AsyncSession, future=True
)


async def get_session() -> Generator:
    session: AsyncSession = SessionLocal()
    try:
        yield session
    finally:
        await session.close()

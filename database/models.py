import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import UUID4, Text, Integer, DateTime, Enums as SQLEnum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enums.enums import Searcher, Language


class Base(AsyncAttrs, DeclarativeBase):
    __mapper_args__ = {'eager_defaults': True}


class User(Base, AsyncAttrs):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID4(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[Language] = mapped_column(SQLEnum(Language), nullable=False, default=Language.ENGLISH)
    search_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    searcher: Mapped[Searcher] = mapped_column(SQLEnum(Searcher), nullable=False, default=Searcher.GOOGLE)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())



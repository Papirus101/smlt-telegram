from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager, AbstractAsyncContextManager
from loguru import logger


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(
            db_url,
            future=True,
        )
        self.session_maker = sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager]:
        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                logger.exception("Session rollback because of exception")
                await session.rollback()
                raise
            finally:
                await session.close()

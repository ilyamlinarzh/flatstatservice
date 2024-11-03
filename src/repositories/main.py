from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import Stub
from fastapi import Depends


class BaseRepository(ABC):
    pass


class SqlalRepository(BaseRepository):
    def __init__(
            self,
            db_session: AsyncSession = Depends(Stub(AsyncSession))
    ):
        self._session = db_session

    async def commit(self):
        await self._session.commit()
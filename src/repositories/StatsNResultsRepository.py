from typing import Sequence, Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.dependencies import Stub
from src.repositories import BaseRepository, SqlalRepository

from sqlalchemy import select, func, Integer, text

from src.models import Results


class StatsNResultsRepository(SqlalRepository):
    async def add_result(
            self,
            ip: str,
            city: str,
            result: str
    ):
        new_result = Results(
            ip=ip,
            city=city,
            result=result
        )
        self._session.add(new_result)

    async def get_total_count(self, **filter_args) -> int:
        total_count_query = select(func.count()).select_from(Results).filter_by(**filter_args)
        total_count = await self._session.execute(total_count_query)
        total_count = total_count.one()[0]
        return total_count

    async def get_city_stat(
            self,
            city: str,
            limit: Optional[int] = None
    ) -> Sequence[Tuple[str, int]]:
        """
        :return: tuple[RESULT, PERCENTAGE_IN_CITY]
        """
        total_count = await self.get_total_count(city=city)
        stat_query = select(
            Results.result,
            (func.round((100 * func.count(Results.result)/total_count), 0)).cast(Integer).label('percentage')
        ).filter_by(city=city).group_by(Results.result).order_by(text('percentage DESC')).limit(limit)

        stat_res = await self._session.execute(stat_query)
        return stat_res.all()

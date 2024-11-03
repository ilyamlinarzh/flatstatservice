from typing import Optional, Sequence

from fastapi import Depends

from src.config import ServiceValues

from src.services import BaseService
from src.repositories import StatsNResultsRepository


class StatsNResultsService(BaseService):
    def __init__(
            self,
            repo: StatsNResultsRepository = Depends()
    ):
        self.repo = repo

    async def get_city_stat(
            self,
            city: str,
            optional_result: Optional[str] = None
    ) -> tuple[Sequence[tuple[str, int]], Optional[int]]:
        """
        :param city: Город из которого нужно получить статистику результатов
        :param optional_result: Опциональный параметр, для получения статистики по конкретному результату отдельно
        :return: Кортеж вида (статистика, процент по опциональному параметру)
        """
        stat = await self.repo.get_city_stat(city)
        limit_stat = stat[:ServiceValues.rating_results_size]
        if optional_result is None:
            return limit_stat, None

        result_percentage = tuple(filter(lambda x: x[0] == optional_result, stat))
        return limit_stat, result_percentage[0][1] if len(result_percentage) != 0 else 0

    # async def __get_result_stat_in_city(self, city: str, result: str) -> int:
    #     total_count = await self.repo.get_total_count(city=city)
    #     result_count = await self.repo.get_total_count(city=city, result=result)
    #     return int(round(100 * (result_count / total_count), 0))

    async def stat_new_result(
            self,
            ip: str,
            city: str,
            result: str
    ):
        await self.repo.add_result(ip, city, result)
        await self.repo.commit()
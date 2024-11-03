from typing import Literal, Optional
from src.config import Cities, ResultsData

from fastapi import APIRouter, Depends

from src.dependencies import id_agent, UserMetadata

from src.services import StatsNResultsService

from .schemas import GetStatResponse

router_stat = APIRouter()


@router_stat.get('/new_result')
async def stat_new_result(
        city: Literal[Cities.access_cities],
        result: Literal[ResultsData.access_results],
        umd: UserMetadata = Depends(id_agent),
        service: StatsNResultsService = Depends()
):
    if umd.access:
        await service.stat_new_result(umd.client_ip, city, result)


@router_stat.get('/get')
async def get_city_stat(
        city: Literal[Cities.access_cities],
        result: Optional[Literal[ResultsData.access_results]] = None,
        service: StatsNResultsService = Depends()
) -> GetStatResponse:
    stat, incity = await service.get_city_stat(city, optional_result=result)
    return GetStatResponse(
        results_stat=stat,
        result_in_city=incity
    )

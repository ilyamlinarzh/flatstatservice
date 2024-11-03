from fastapi import APIRouter
from src.api.v1.stat.router import router_stat

router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(router_stat, prefix='/stat')
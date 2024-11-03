from typing import Annotated, Tuple
from redis.asyncio import Redis

from dataclasses import dataclass

from fastapi import Depends

from src.dependencies import Stub

from src.repositories import BaseRepository

import time

from src.config import RateLimits

RedisKey = Annotated[Tuple[str, int], "Строки-ключи с возможностью форматирования, + expire value"]


class IdAgentRepository(BaseRepository):
    @dataclass
    class RedisKeys:
        ip_traces: RedisKey = ("ip_traces:{ip}", RateLimits.ip_expire)

    def __init__(self,
                 redis: Redis = Depends(Stub(Redis))
                 ):
        self.__redis = redis

    async def ip_has_traces(self, ip) -> bool:
        res = await self.__redis.exists(
            self.RedisKeys.ip_traces[0].format(ip=ip)
        )
        return bool(res)

    async def ip_traces_count(self, ip) -> int:
        return await self.__redis.hlen(
            self.RedisKeys.ip_traces[0].format(ip=ip)
        )

    async def get_ip_traces(self, ip: str) -> dict:
        return await self.__redis.hgetall(
            self.RedisKeys.ip_traces[0].format(ip=ip)
        )

    async def ip_has_this_trace(self, ip: str, trace: str):
        return await self.__redis.hexists(
            self.RedisKeys.ip_traces[0].format(ip=ip),
            trace,
        )

    async def add_ip_trace(self, ip: str, trace: str):
        await self.__redis.hset(
            self.RedisKeys.ip_traces[0].format(ip=ip),
            trace,
            str(int(time.time()))
        )

    async def set_ip_expire(self, ip: str):
        await self.__redis.expire(
            self.RedisKeys.ip_traces[0].format(ip=ip),
            self.RedisKeys.ip_traces[1]
        )

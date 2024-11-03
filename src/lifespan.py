from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.redis import get_redis, create_redis_pool

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_pool = create_redis_pool()
    redis = get_redis(redis_pool)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

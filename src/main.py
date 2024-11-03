from fastapi import FastAPI, Request
from src.db import create_session_maker, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.redis import get_redis, create_redis_pool
from redis.asyncio import Redis

from src.initializers import dependencies_init, dependencies_list

from functools import partial

from src.lifespan import lifespan

from src.api.v1 import router_v1


def create_app():
    app = FastAPI(lifespan=lifespan)

    db_sessionmaker = create_session_maker()
    redis_pool = create_redis_pool()

    deps: dependencies_list = [
        (AsyncSession, partial(get_async_session, db_sessionmaker)),
        (Redis, partial(get_redis, redis_pool)) # redis.asyncio.Redis
    ]

    dependencies_init(app, deps)

    app.include_router(router_v1)

    return app


app = create_app()
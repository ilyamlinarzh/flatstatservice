from redis.asyncio import Redis, ConnectionPool
from config import settings


def create_redis_pool() -> ConnectionPool:
    pool = ConnectionPool.from_url(
        url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        decode_responses=True
    )

    return pool


def get_redis(pool: ConnectionPool) -> Redis:
    return Redis(
        connection_pool=pool
    )

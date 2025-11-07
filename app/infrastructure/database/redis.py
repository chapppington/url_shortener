from redis.asyncio import Redis

from settings import config


redis = Redis(
    host=config.redis_host,
    port=config.redis_port,
    decode_responses=True,
)

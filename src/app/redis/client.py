import redis
from loguru import logger


MAX_VALUE_SIZE = 10 * 1024 * 1024  # Максимальный объем значения 10 МБ


class RedisClient:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host='redis',
            port=6379,
            db=0,
            max_connections=10,
            socket_timeout=3,
            socket_keepalive=True,
        )

    def __enter__(self):
        self.redis_cli = redis.Redis(connection_pool=self.pool)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.redis_cli.connection_pool.disconnect()

    def get_value(self, user_id: str, key: str):
        value = self.redis_cli.hget(f'user:{user_id}', key)
        if value is None:
            logger.exception(
                f'Attempt to take a non-existent '
                f'value {value} by user {user_id}.'
            )
            return None
        return value.decode()

    def set_value(self, user_id: str, key: str, value: str):
        self.redis_cli.hset(f'user:{user_id}', key, value)
        logger.info(f'Set {key}:{value} for user {user_id}.')

    def delete_value(self, user_id: str, key: str):
        self.redis_cli.hdel(f'user:{user_id}', key)
        logger.info(f'Removed value under key {key} by user {user_id}.')

    def value_exists(self, user_id: str, key: str):
        return self.redis_cli.hexists(f'user:{user_id}', key)

    def get_all_values(self, user_id):
        all_values = self.redis_cli.hgetall(f'user:{user_id}')
        return {
            key.decode(): value.decode() for key, value in all_values.items()
        }

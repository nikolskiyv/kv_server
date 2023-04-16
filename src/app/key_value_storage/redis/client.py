import redis
from loguru import logger

from src.app.key_value_storage.base import BaseKeyValueStorage
from src.common import settings


class RedisClient(BaseKeyValueStorage):

    def __init__(self):
        """ Создание пула соединений к Redis """
        self.pool = redis.ConnectionPool(
            host='redis',
            port=settings.REDIS_PORT,
            db=0,
            max_connections=1000,
            socket_timeout=settings.REDIS_SOCKET_CONNECTION_TIMEOUT,
            socket_keepalive=settings.REDIS_SOCKET_KEEPALIVE,
        )

    def __enter__(self):
        """
        Получение соединения из пула
        """
        self.redis_cli = redis.Redis(connection_pool=self.pool)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Возвращение соединения в пул
        """
        self.redis_cli.connection_pool.disconnect()

    def hget_value(self, user_id: str, key: str):
        """
        Получение значение из хэша пользователя по его ключу
        Хэш пользователя хранится под ключом user:<user_id>
        """
        value = self.redis_cli.hget(f'user:{user_id}', key)
        if value is None:
            logger.exception(
                f'Attempt to take a non-existent '
                f'value {value} by user {user_id}.'
            )
            return None
        return value.decode()

    def hset_value(self, user_id: str, key: str, value: str):
        """
        Установка значения в хэш пользователя по его ключу
        """
        self.redis_cli.hset(f'user:{user_id}', key, value)
        logger.info(f'Set value for user {user_id}.')

    def hdel_value(self, user_id: str, key: str):
        """
        Удаление значения из хэша пользователя по его ключу
        """
        self.redis_cli.hdel(f'user:{user_id}', key)
        logger.info(f'Remove value by user {user_id}.')

    def hexists(self, user_id: str, key: str):
        """
        Проверка на то, содержит ли пользователь значение под
        заданным ключом
        """
        return self.redis_cli.hexists(f'user:{user_id}', key)

    def hget_all_values(self, user_id):
        """
        Получение всех значений пользователя
        """
        all_values = self.redis_cli.hgetall(f'user:{user_id}')
        return {
            key.decode(): value.decode() for key, value in all_values.items()
        }

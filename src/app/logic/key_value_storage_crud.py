from werkzeug.exceptions import NotFound, BadRequest

from src.app.key_value_storage.redis import redis_cli
from src.app.models import KeyValueResponse


class KeyValueStorageCrud:
    storage_cli = redis_cli

    @classmethod
    def get_value(cls, user_id, key):
        with cls.storage_cli as conn:
            value = conn.hget_value(user_id, key)
            if value is None:
                raise NotFound('Value not found')
        return KeyValueResponse(key=key, value=value)

    @classmethod
    def create_value(cls, user_id, key, value):
        with cls.storage_cli as conn:
            if conn.hexists(user_id, key):
                raise BadRequest('Value already exists')
            conn.hset_value(user_id, key, value)
        return KeyValueResponse(key=key, value=value)

    @classmethod
    def update_value(cls, user_id, key, value):
        with cls.storage_cli as conn:
            if not conn.hexists(user_id, key):
                raise NotFound('Value not found')
            conn.hset_value(user_id, key, value)
        return KeyValueResponse(key=key, value=value)

    @classmethod
    def delete_value(cls, user_id, key):
        with cls.storage_cli as conn:
            value = conn.hget_value(user_id, key)
            if value is None:
                raise NotFound('Value not found')
            conn.hdel_value(user_id, key)
        return KeyValueResponse(key=key, value=value)

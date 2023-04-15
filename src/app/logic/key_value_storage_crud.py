from flask import jsonify
from werkzeug.exceptions import NotFound, BadRequest

from src.app.key_value_storage.redis import redis_cli


class KeyValueStorageCrud:
    storage_cli = redis_cli

    @classmethod
    def get_value(cls, user_id, key):
        with cls.storage_cli as conn:
            value = conn.hget_value(user_id, key)
            if value is None:
                raise NotFound('Value not found')
            return jsonify({'value': value}), 200

    @classmethod
    def create_value(cls, user_id, key, value):
        if not key:
            raise BadRequest('No key provided')
        if not value:
            raise BadRequest('No value provided')
        with cls.storage_cli as conn:
            if conn.hexists(user_id, key):
                raise BadRequest('Value already exists')
            conn.hset_value(user_id, key, value)
            return jsonify({'status': 'ok'}), 201

    @classmethod
    def update_value(cls, user_id, key, value):
        if not value:
            raise BadRequest('No value provided')
        with cls.storage_cli as conn:
            if not conn.hexists(user_id, key):
                raise NotFound('Value not found')
            conn.hset_value(user_id, key, value)
            return jsonify({'status': 'ok'}), 200

    @classmethod
    def delete_value(cls, user_id, key):
        with cls.storage_cli as conn:
            if not conn.hexists(user_id, key):
                raise NotFound('Value not found')
            conn.hdel_value(user_id, key)
            return jsonify({'status': 'ok'}), 200

    @classmethod
    def get_all_values(cls, user_id):
        with cls.storage_cli as conn:
            values = conn.hget_all_values(user_id)
            return jsonify({'values': values}), 200
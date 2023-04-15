from flask import (
    jsonify,
    request,
)
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
)

from . import bp
from .helpers import validate_uuid
from ..models import KeyValue
from ..redis import redis_cli


@bp.route('/health', methods=['GET'])
def health_check():
    """ Проверка жизнеспособности сервиса """
    return jsonify({'status': 'ok'}), 200


@bp.route('/users/<user_id>/keys/<key>', methods=['GET'])
@validate_uuid
def get_value(user_id: str, key: str):
    """ Получение значение пользователя """
    with redis_cli as conn:
        value = conn.get_value(user_id, key)
        if value is None:
            raise NotFound('Value not found')
        return jsonify({'value': value}), 200


@bp.route('/users/<user_id>', methods=['GET'])
@validate_uuid
def get_all_values(user_id: str):
    """ Получение всех значений пользователя """
    with redis_cli as conn:
        values = conn.get_all_values(user_id)
        return jsonify({'values': values}), 200


@bp.route('/users/<user_id>/keys/<key>', methods=['PUT'])
@validate_uuid
def update_value(user_id: str, key: str):
    """ Обновление значения """
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided')

    data = KeyValue(**data)
    value = data.value
    if value is None:
        raise BadRequest('No value provided')
    with redis_cli as conn:
        if not conn.value_exists(user_id, key):
            raise NotFound('Value not found')
        conn.set_value(user_id, key, value)
        return jsonify({'status': 'ok'}), 200


@bp.route('/users/<user_id>/keys/<key>', methods=['DELETE'])
@validate_uuid
def delete_value(user_id: str, key: str):
    """ Удаление значения """
    with redis_cli as conn:
        if not conn.value_exists(user_id, key):
            raise NotFound('Value not found')
        conn.delete_value(user_id, key)
        return jsonify({'status': 'ok'}), 200


@bp.route('/users/<user_id>', methods=['POST'])
@validate_uuid
def create_value(user_id: str):
    """ Создание значения """
    data = request.get_json()
    if not data:
        raise BadRequest('No data provided')

    data = KeyValue(**data)
    key = data.key
    value = data.value
    if not key:
        raise BadRequest('No key provided')
    if not value:
        raise BadRequest('No value provided')
    with redis_cli as conn:
        if conn.value_exists(user_id, key):
            raise BadRequest('Value already exists')
        conn.set_value(user_id, key, value)
        return jsonify({'status': 'ok'}), 201

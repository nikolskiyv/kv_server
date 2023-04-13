import redis
from flask import Blueprint, jsonify

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

bp = Blueprint('api', __name__)  # url_prefix='/api')

pool = redis.ConnectionPool(
        host='localhost',
        port=6379,
        db=0,
        max_connections=10,
        socket_timeout=3,
        socket_keepalive=True,
    )


def create_redis_cli():
    redis_cli = redis.Redis(connection_pool=pool)

    return redis_cli


r = create_redis_cli()


class ValidateUserInputs(Inputs):
    json = [JsonSchema({
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'value': {'type': 'string'},
            'user_id': {'type': 'string'}
        },
        'required': ['key']
    })]


@bp.route('/health', methods=['GET'])
def health_check():
    return 'ok', 200


@bp.route('/users/<user_id>/keys/<key>', methods=['GET'])
def get_key(user_id, key):
    """Получение значения ключа"""


    value = r.get(f'{user_id}:{key}')
    if value is None:
        return '', 404
    return value.decode(), 200


@bp.route('/users/<user_id>/keys/<key>/<value>', methods=['POST'])
def add_key(user_id, key, value):
    value = value
    if r.exists(f'{user_id}:{key}'):
        r.set(f'{user_id}:{key}', value)
        return '', 204
    else:
        return '', 404


@bp.route('/users/<user_id>/keys/<key>', methods=['PUT'])
def update_key(user_id, key):
    pass


@bp.route('/users/<user_id>/keys/<key>', methods=['DELETE'])
def delete_key(user_id, key):
    pass


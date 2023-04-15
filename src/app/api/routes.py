from flask import jsonify

from . import bp
from ..logic.redis_crud import RedisCrud
from ..models import UserKey, UserID, UserData

from flask_pydantic import validate


@bp.route('/health', methods=['GET'])
def health_check():
    """ Проверка жизнеспособности сервиса """
    return jsonify({'status': 'ok'}), 200


@bp.route('/value', methods=['GET'])
@validate()
def get_value(query: UserKey):
    """ Получение значение пользователя """
    return RedisCrud.get_value(query.user_id, query.key)


@bp.route('/values', methods=['GET'])
@validate()
def get_all_values(query: UserID):
    """ Получение всех значений пользователя """
    return RedisCrud.get_all_values(query.user_id)


@bp.route('/value', methods=['PUT'])
@validate()
def update_value(body: UserData):
    """ Обновление значения """
    return RedisCrud.update_value(body.user_id, body.key, body.value)


@bp.route('/value', methods=['DELETE'])
@validate()
def delete_value(query: UserKey):
    """ Удаление значения """
    return RedisCrud.delete_value(query.user_id, query.key)


@bp.route('/value', methods=['POST'])
@validate()
def create_value(body: UserData):
    """ Создание значения """
    return RedisCrud.create_value(body.user_id, body.key, body.value)

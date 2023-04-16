from flask import jsonify

from . import bp
from ..logic.key_value_storage_crud import KeyValueStorageCrud
from src.app.api.models import UserKey, UserID, UserData

from flask_pydantic import validate


@bp.route('/health', methods=['GET'])
def health_check():
    """ Проверка жизнеспособности сервиса """
    return jsonify({'status': 'ok'}), 200


@bp.route('/storage', methods=['GET'])
@validate()
def get_value(query: UserKey):
    """ Получение значение пользователя """
    value = KeyValueStorageCrud.get_value(query.user_id, query.key)
    return jsonify({'value': value}), 200


@bp.route('/storage', methods=['GET'])
@validate()
def get_all_values(query: UserID):
    """ Получение всех значений пользователя """
    values = KeyValueStorageCrud.get_all_values(query.user_id)
    return jsonify({'values': values}), 200


@bp.route('/storage', methods=['PUT'])
@validate()
def update_value(body: UserData):
    """ Обновление значения """
    KeyValueStorageCrud.update_value(body.user_id, body.key, body.value)
    return jsonify({'status': 'ok'}), 200


@bp.route('/storage', methods=['DELETE'])
@validate()
def delete_value(query: UserKey):
    """ Удаление значения """
    KeyValueStorageCrud.delete_value(query.user_id, query.key)
    return jsonify({'status': 'ok'}), 200


@bp.route('/storage', methods=['POST'])
@validate()
def create_value(body: UserData):
    """ Создание значения """
    KeyValueStorageCrud.create_value(body.user_id, body.key, body.value)
    return jsonify({'status': 'ok'}), 200

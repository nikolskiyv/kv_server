from flask import Blueprint, jsonify, make_response
from werkzeug.exceptions import NotFound

bp = Blueprint('api', __name__)  # url_prefix='/api')


@bp.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'error': str(e)}), 404


@bp.errorhandler(Exception)
def handle_pydantic_validation_error(e):
    return jsonify({'message': str(e)}), 400

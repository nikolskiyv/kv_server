from flask import Blueprint, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import NotFound, BadRequest

bp = Blueprint('api', __name__)


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'message': str(e.description)}), 400


@bp.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'message': str(e.description)}), 404


@bp.errorhandler(ValidationError)
def handle_pydantic_validation_error(e):
    return jsonify({'message': str(e.description)}), 400

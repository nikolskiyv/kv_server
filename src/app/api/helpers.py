import uuid
from functools import wraps
from werkzeug.exceptions import BadRequest


def validate_uuid(f):
    """
    В API user_id должен быть в uuid.
    Если это не так, то возвращаем ошибку BadRequest.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise BadRequest('Invalid UUID')
        return f(*args, **kwargs)
    return wrapper

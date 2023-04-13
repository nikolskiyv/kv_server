import uuid
from time import time

from flask import Flask, Blueprint, g, request
from loguru import logger


def get_request_ip():
    return request.headers.get('X-Real-Ip') or request.remote_addr


def get_request_context():
    return {
        'ip': get_request_ip(),
        'host': request.host.split(':', 1)[0],
        'method': request.method,
        'path': request.path,
        'user_agent': str(request.user_agent),
    }


def get_duration(start):
    return (time() - start) * 1000


def register(app: Flask):
    bp = Blueprint('log', __name__)

    @bp.before_app_request
    def before_request():
        g.reqid = uuid.uuid4().hex
        g.start = time()
        logger.debug('HTTP request started', **get_request_context())

    @bp.after_app_request
    def after_request(response):
        ctx = get_request_context()
        duration = get_duration(g.start)
        ctx.update({'status_code': response.status_code, 'duration': duration})

        if response.status_code >= 400:
            logger.error(f'HTTP request failed: {response.status_code}')

        logger.debug('HTTP request finished', **ctx)
        return response

    app.logger = logger
    app.register_blueprint(bp)

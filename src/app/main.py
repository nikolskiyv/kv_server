import sys

from flask import Flask, request
from loguru import logger

from src.app.api.routes import bp
from src.common import settings


import logging
from flask.logging import default_handler


def create_app():
    flask_app = Flask(settings.APP or __name__)

    flask_app.config['DEBUG'] = settings.DEBUG

    flask_app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
    flask_app.config['SECRET_KEY'] = settings.SECRET_KEY

    flask_app.register_blueprint(bp)

    flask_app.logger.removeHandler(default_handler)
    flask_app.logger.setLevel(logging.INFO)

    logger.remove()
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSSSSS} |"
               " {level} | {name} | {message}"
    )

    @flask_app.before_request
    def log_request():
        logger.info(
            "Request received: {} {}".format(request.method, request.path)
        )

    @flask_app.after_request
    def log_response(response):
        logger.info("Response sent: {}".format(response.status))
        return response

    logger.info("Application started successfully!")

    return flask_app


app = create_app()

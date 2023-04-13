from flask import Flask

from src.app.api.routes import bp
from src.common import settings

# import logging as flask_logging

# from common import settings


def create_app():
    flask_app = Flask(settings.APP or __name__)

    flask_app.config['DEBUG'] = settings.DEBUG
    flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    flask_app.config['JSON_AS_ASCII'] = False

    # app.logger.disabled = True
    # log = flask_logging.getLogger('werkzeug')
    # log.disabled = True

    # logging.register(app)

    flask_app.register_blueprint(bp)
    # logging.register(app)

    return flask_app


app = create_app()

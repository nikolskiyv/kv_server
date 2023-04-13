from flask import Flask

from storage_api.v1 import bp


# from common import settings


def create_app():
    app = Flask(__name__)
    # app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    # _app.config.from_object("config")

    app.register_blueprint(bp)
    # logging.register(app)

    return app


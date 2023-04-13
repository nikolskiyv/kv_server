import os

from main import app
from src.common import settings


def run():
    app.run(host='0.0.0.0',
            port=int(os.getenv('APP_PORT', '8080')),
            debug=settings.DEBUG)


run()

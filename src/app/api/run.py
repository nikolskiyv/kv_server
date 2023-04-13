import os

from main import create_app


def run():
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', '8080')))


run()

import pytest

from src.app.main import create_app
from src.app.key_value_storage.redis import RedisClient


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def redis_client():
    with RedisClient() as client:
        yield client


@pytest.fixture(autouse=True)
def setup_method(redis_client):
    redis_client.redis_cli.flushdb()

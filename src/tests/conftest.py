import pytest
import redis

from src.app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def redis_server():
    # Запуск тестового Redis-сервера перед запуском тестов
    server = redis.server.RedisServer()
    server.start()

    yield server

    # Остановка Redis-сервера после окончания тестов
    server.stop()


@pytest.fixture(scope="function")
def redis_client(redis_server):
    # Создание тестовой базы данных Redis
    client = redis.Redis(host=redis_server.host, port=redis_server.port, db=0)

    # Удаление всех данных перед запуском каждого теста
    client.flushall()

    yield client

    # Очистка базы данных после завершения каждого теста
    client.flushall()


@pytest.fixture
def test_data():
    return {
        'user_id': 'test_user',
        'key': 'test_key',
        'value': 'test_value'
    }

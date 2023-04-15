from http import HTTPStatus


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}


def test_create_value(client, test_data):
    # Ensure the value does not exist
    response = client.get(f'/api/users/{test_data["user_id"]}/keys/{test_data["key"]}')
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.post(f'/api/users/{test_data["user_id"]}', json=test_data)
    assert response.status_code == HTTPStatus.CREATED

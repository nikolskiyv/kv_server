import pytest

from src.common import settings

VALID_UUID = '123e4567-e89b-12d3-a456-426655440000'
ANOTHER_VALID_UUID = '123e4567-e89b-23d3-a456-426655440999'
INVALID_UUID = 'not_a_uuid'


def test_get_value_from_another_user(client):
    data1 = {'user_id': VALID_UUID, 'key': 'key1', 'value': 'value1'}
    response1 = client.post('/value', json=data1)
    assert response1.status_code == 201

    response2 = client.get(f'/value?user_id={ANOTHER_VALID_UUID}&key=key1')
    assert response2.status_code == 404


@pytest.mark.parametrize('user_id, key, value', [
    (VALID_UUID, 'test_key', 'test_value'),
], ids=['short_value'])
def test_create_value(client, user_id, key, value):
    data = {'user_id': user_id, 'key': key, 'value': value}
    response = client.post('/value', json=data)
    assert response.status_code == 201


@pytest.mark.parametrize('user_id, key, value', [
    (VALID_UUID, 'test_key', 'test_value'*settings.MAX_VALUE_SIZE),
], ids=['long_value'])
def test_create_large_value(client, user_id, key, value):
    data = {'user_id': user_id, 'key': key, 'value': value}
    response = client.post('/value', json=data)
    assert response.status_code == 201


@pytest.mark.parametrize('user_id, key, value', [
    (INVALID_UUID, 'test_key', 'test_value'),
    (INVALID_UUID, '', 'test_value'),
    (INVALID_UUID, 'test_key', ''),
    (INVALID_UUID, 'test_key', 'a' * 1001),
], ids=['base', 'empty key', 'empty value', 'long_value'])
def test_try_to_create_value_with_invalid_user_id(client, user_id, key, value):
    data = {'user_id': user_id, 'key': key, 'value': value}
    response = client.post('/value', json=data)
    assert response.status_code == 400


@pytest.mark.parametrize('user_id, key', [
    (VALID_UUID, 'test_key'),
])
def test_get_value(client, user_id, key):
    data = {'user_id': user_id, 'key': key, 'value': 'value'}
    client.post('/value', json=data)

    response = client.get(f'/value?user_id={user_id}&key={key}')
    assert response.status_code == 200


@pytest.mark.parametrize('user_id, key', [
    (VALID_UUID, 'nonexistent_key'),
])
def test_try_to_get_not_existed_value(client, user_id, key):
    response = client.get(f'/value?user_id={user_id}&key={key}')
    assert response.status_code == 404


@pytest.mark.parametrize('user_id, key, value', [
    (VALID_UUID, 'test_key', 'test_value'),
], ids=['base'])
def test_update_value(client, user_id, key, value):
    data = {'user_id': user_id, 'key': key, 'value': value}
    client.post('/value', json=data)

    updated_data = {'user_id': user_id, 'key': key, 'value': 'new_value'}
    response = client.put(
        '/value?user_id={user_id}&key={key}', json=updated_data)
    assert response.status_code == 200


@pytest.mark.parametrize('user_id, key, value', [
    (VALID_UUID, 'no_existed_test_key', 'test_value'),
], ids=['base'])
def test_try_to_update_no_exists_value(client, user_id, key, value):
    data = {'user_id': user_id, 'key': key, 'value': value}
    response = client.put(f'/value?user_id={user_id}&key={key}', json=data)
    assert response.status_code == 404


@pytest.mark.parametrize('user_id, key', [
    (VALID_UUID, 'test_key'),
], ids=['base'])
def test_delete_value(client, user_id, key):
    data = {'user_id': user_id, 'key': key, 'value': 'value'}
    client.post('/value', json=data)

    response = client.delete(f'/value?user_id={user_id}&key={key}')
    assert response.status_code == 200


@pytest.mark.parametrize('user_id, key', [
    (VALID_UUID, 'test_key'),
], ids=['base'])
def test_try_to_delete_not_existed_value(client, user_id, key):
    response = client.delete(f'/value?user_id={user_id}&key={key}')
    assert response.status_code == 404

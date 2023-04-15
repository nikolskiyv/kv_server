def test_set_value(redis_client):
    user_id = 'test_user'
    key = 'test_key'
    value = 'test_value'

    redis_client.set_value(user_id, key, value)
    assert redis_client.redis_cli.hget(
        f'user:{user_id}', key).decode() == value


def test_get_value(redis_client):
    user_id = 'test_user'
    key = 'test_key'
    value = 'test_value'

    # Check for non-existent key
    assert redis_client.get_value(user_id, key) is None

    # Set a value and check that it is returned
    redis_client.set_value(user_id, key, value)
    assert redis_client.get_value(user_id, key) == value


def test_value_exists(redis_client):
    user_id = 'test_user'
    key = 'test_key'
    value = 'test_value'

    # Check for non-existent key
    assert not redis_client.value_exists(user_id, key)

    # Set a value and check that it exists
    redis_client.set_value(user_id, key, value)
    assert redis_client.value_exists(user_id, key)


def test_delete_value(redis_client):
    user_id = 'test_user'
    key = 'test_key'
    value = 'test_value'

    # Set a value and delete it
    redis_client.set_value(user_id, key, value)
    redis_client.delete_value(user_id, key)

    # Check that the key no longer exists
    assert not redis_client.value_exists(user_id, key)

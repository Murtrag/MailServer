import pytest
import users


@pytest.mark.user
@pytest.mark.parametrize(
    "username, password",
    [
        ("kajtek", "test12311"),
        ("bart123", "123tes11t"),
        ("test3", "test3111"),
    ],
)
def test_create_user(username, password):
    assert users.create_user(username, password) is not None
    assert username in users.get_users()


@pytest.mark.user
@pytest.mark.parametrize(
    "username, password, new_password",
    [
        ("kajtek", "test12311", "test12345"),
        ("bart123", "123tes11t", "test12345"),
        ("test3", "test3111", "test12345"),
    ],
)
def test_change_password(username, password, new_password):
    users.change_password(username, password, new_password)
    assert username in users.get_users()


@pytest.mark.user
@pytest.mark.parametrize(
    "username, password",
    [
        ("kajtek", "test12345"),
        ("bart123", "test12345"),
        ("test3", "test12345"),
    ],
)
def test_remove_user(username, password):
    users.remove_user(username, password)
    assert username not in users.get_users()


@pytest.mark.user
def test_get_users():
    assert type(users.get_users()) == list

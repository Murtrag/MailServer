import pytest

from database import (
    get_connection,
    get_cursor,
    domain_name,
    user,
    password,
    db_name,
    db_server,
)


@pytest.mark.connection
def test_variables():
    assert type(user) == str

    assert type(password) == str

    assert type(db_name) == str
    assert len(db_name) > 1

    assert type(db_server) == str
    assert len(db_server) >= 2

    assert type(domain_name) == str
    assert len(domain_name) > 2


@pytest.mark.connection
def test_get_connection(db_connection):
    assert db_connection.status == 1


@pytest.mark.connection
def test_get_cursor(db_connection):
    cursor = get_cursor(db_connection)
    sql = """SELECT id, sender, title, message FROM messages where receiver=%s ORDER BY creation_date;"""
    cursor.execute(sql, (f"test@{domain_name}",))
    assert len(cursor.fetchall()) == 0  # @TODO Create fixture & inc this number

from database import get_connection, get_cursor, domain_name
import pytest


@pytest.mark.connection
def test_get_connection():
	assert get_connection().status == 1

@pytest.mark.connection
def test_get_cursor():
	cursor = get_cursor(get_connection())
	sql = """SELECT id, sender, title, message FROM messages where receiver=%s ORDER BY creation_date;"""
	cursor.execute(sql, (f"test@{domain_name}",))
	assert len(cursor.fetchall()) == 0 # @TODO Create fixture & inc this number 



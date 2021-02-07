import pytest
from database import get_connection, get_cursor

@pytest.fixture
def db_connection(scope='module'):
	return get_connection()

from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor


def get_connection():
    try:
        cnx = connect(user="postgres", password="coderslab", host="127.0.0.1", database="workshops")
        cnx.autocommit = True
        return cnx
    except OperationalError as error:
        print(error)


def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)

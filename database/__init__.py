from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor
from configparser import ConfigParser
import os
parser = ConfigParser()
parser.read('database/config.ini')
# print(parser.sections())
user = parser['db']['username']
password = parser['db']['password']
db_name = parser['db']['name']

def get_connection():
    try:
        cnx = connect(user=user, password=password, host="127.0.0.1", database=db_name)
        cnx.autocommit = True
        return cnx
    except OperationalError as error:
        print(error)


def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)

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
server_name = parser['db']['server']
domain_name = parser['db']['domain']

def get_connection():
    try:
        cnx = connect(user=user, password=password, host=server_name, database=db_name)
        cnx.autocommit = True
        return cnx
    except OperationalError as error:
        print(error)


def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)

import os

from configparser import ConfigParser
from psycopg2.extras import RealDictCursor
from psycopg2 import connect, OperationalError

parser = ConfigParser()
parser.read("database/config.ini")
user = parser["db"]["username"]
password = parser["db"]["password"]
db_name = parser["db"]["db_name"]
db_server = parser["db"]["db_server"]
domain_name = parser["db"]["domain"]


def get_connection():
    try:
        cnx = connect(user=user, password=password, host=db_server, database=db_name)
        cnx.autocommit = True
        return cnx
    except OperationalError as error:
        print("Connection error: ", error)
        return None


def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)

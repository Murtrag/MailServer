from models import User
from database import get_connection, get_cursor

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)

    # user = User()
    # user.username = 'Janusz'
    # user.email = 'janusz@asd.pl'
    # user.set_password('tajne123')
    # user.save_to_db(cursor)

    user = User.load_user_by_id(cursor, 4)
    user.delete(cursor)

    # users = User.load_all_users(cursor)
    # print(users)

    connection.close()

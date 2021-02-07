import sys
import clcrypto

from models import User
from database import get_connection, get_cursor, domain_name

connection = get_connection()
cursor = get_cursor(connection)


def create_user(username, password):
    print("-----------------Tworzymy usera-----------------------")
    if User.load_users_by_any(cursor, username=username):
        print("błąd: Taki użytkownik już istnieje ;(")
    elif clcrypto.check_pass_len(password):
        user = User()
        user.username = username
        user.email = f"{username}@{domain_name}"
        user.set_password(password, salt="asdf123")
        user.save_to_db(cursor)
    else:
        print("Podane hasło zbyt krótkie")


def change_password(username, old_password, new_password):
    get_user = User.load_users_by_any(cursor, username=username)[0]
    if get_user:
        if clcrypto.check_password(old_password, get_user.hashed_password):
            if clcrypto.check_pass_len(new_password):
                get_user.set_password(new_password)
                get_user.save_to_db(cursor)
                print("hasło zostało zmienione")
            else:
                print("Podane hasło jest zbyt słabe")
        else:
            print("podsałeś błędne hasło")
    else:
        print("Nie znaleziono użytkownika")


def remove_user(username, password):
    try:
        get_user = User.load_users_by_any(cursor, username=username)[0]
    except IndexError:
        print("Podany user nie istnieje")
        exit(1)
    if get_user:
        if clcrypto.check_password(password, get_user.hashed_password):
            get_user.delete(cursor)
            print("usunięto usera z bazy")
        else:
            print("błędne hasło")


def get_users():
    users = User().load_all_users(cursor)
    return [x.username for x in users]


if __name__ == "__main__":
    if connection is None:
        exit(0)

    pairs = clcrypto.slice_args(sys.argv)

    if (
        len(set(("-u", "-p")) & set(pairs)) == 2
        and len(set(("-e", "-d")) & set(pairs)) < 1
    ):
        """ create user"""
        # python3 main.py -u franek12 -p tajne123
        username = pairs["-u"]
        password = pairs["-p"]
        create_user(username, password)

    elif len(set(("-u", "-p", "-e", "-n")) & set(pairs)) == 4:
        """ change password"""
        # python3 main.py -u franek12 -p tajne123 -e -n tajne1234
        username = pairs["-u"]
        password = pairs["-p"]
        new_password = pairs["-n"]
        change_password(username, password, new_password)

    elif len(set(("-u", "-p", "-d")) & set(pairs)) == 3:
        """remove user from db"""
        # python3 main.py -u franek12 -p tajne1234 -d
        username = pairs["-u"]
        password = pairs["-p"]

        remove_user(username, password)

    elif set(("-l",)) == set(pairs):
        """ print all users """
        print("\n".join(get_users()))

    else:
        print("komunikat pomocy \n")

        print("     -l  Wyświetl wszystkich dostępnych używkowników \n")

        print("     -u & -p  Utwurz nowego użytkownika e.g.")
        print("     python3 main.py -u franek12 -p tajne123 \n\n")

        print("     -u & -p & -e & -n Zmień hasło użytkownikowi e.g.")
        print("     python3 main.py -u franek12 -p tajne123 -e -n tajne1234\n\n")

        print("     -u & -p & -d Usuń użytkownika z bazy danych")
        print("     python3 main.py -u franek12 -p tajne1234 -d")

    connection.close()

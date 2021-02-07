import sys
import clcrypto

from models import User
from database import get_connection, get_cursor, domain_name

connection = get_connection()
cursor = get_cursor(connection)


def create_user(username, password):
    if User.filter(cursor, username=username) != []:
        print("błąd: Taki użytkownik już istnieje ;(")
        return None

    elif clcrypto.check_pass_len(password):
        print("-----------------Tworzymy usera-----------------------")
        user = User()
        user.username = username
        user.email = f"{username}@{domain_name}"
        user.set_password(password, salt="asdf123")
        user.save_to_db(cursor)
        return user

    else:
        print("Podane hasło zbyt krótkie")
        return None


def change_password(username, old_password, new_password):
    get_user = User.filter(cursor, username=username)[0]

    if get_user is None:
        print("Nie znaleziono użytkownika")
        return None

    if clcrypto.check_password(old_password, get_user.hashed_password) is False:
        print("Podałeś błędne hasło")
        return None

    if clcrypto.check_pass_len(new_password) is False:
        print("Podane hasło jest zbyt słabe")
        return None

    get_user.set_password(new_password)
    get_user.save_to_db(cursor)
    print("hasło zostało zmienione")


def remove_user(username, password):
    try:
        get_user = User.filter(cursor, username=username)[0]
    except IndexError:
        print("Podany user nie istnieje")
        return None

    if clcrypto.check_password(password, get_user.hashed_password) is False:
        print("błędne hasło")
        return None

    get_user.delete(cursor)
    print("usunięto usera z bazy")


def get_users():
    users = User().load_all_users(cursor)
    return [x.username for x in users]


if __name__ == "__main__":
    if connection is None:
        exit(0)

    pairs = clcrypto.slice_args(sys.argv)
    pairs_keys = pairs.keys()

    if all(param in pairs_keys for param in ("-u", "-p", "-e", "-n")):
        """ change password"""
        # python3 main.py -u franek12 -p tajne123 -e -n tajne1234
        username = pairs["-u"]
        password = pairs["-p"]
        new_password = pairs["-n"]
        change_password(username, password, new_password)

    elif all(param in pairs_keys for param in ("-u", "-p", "-d")):
        """remove user from db"""
        # python3 main.py -u franek12 -p tajne1234 -d
        username = pairs["-u"]
        password = pairs["-p"]

        remove_user(username, password)

    elif all(param in pairs_keys for param in ("-u", "-p")):
        """ create user"""
        # python3 main.py -u franek12 -p tajne123
        username = pairs["-u"]
        password = pairs["-p"]
        create_user(username, password)

    elif all(param in pairs_keys for param in ("-l")):
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

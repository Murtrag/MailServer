#!/usr/local/bin/python3
import sys
import clcrypto

from models import User
from database import get_connection, get_cursor, domain_name

connection = get_connection()
cursor = get_cursor(connection)


def create_user(username, password):
    if User.filter(cursor, username=username) != []:
        print("This user already exists.")
        return None

    elif clcrypto.check_pass_len(password):
        user = User()
        user.username = username
        user.email = f"{username}@{domain_name}"
        user.set_password(password, salt="asdf123")
        user.save_to_db(cursor)
        print("User has been created.")
        return user

    else:
        print("This password is to short.")
        print("Password should contains at least 8 chars")
        return None


def change_password(username, old_password, new_password):
    get_user = User.filter(cursor, username=username)[0]

    if get_user is None:
        print("User doas not exist.")
        return None

    if clcrypto.check_password(old_password, get_user.hashed_password) is False:
        print("This password is incorrect.")
        return None

    if clcrypto.check_pass_len(new_password) is False:
        print("This password is to short.")
        print("Password should contains at least 8 chars.")
        return None

    get_user.set_password(new_password)
    get_user.save_to_db(cursor)
    print("Password has been changed.")


def remove_user(username, password):
    try:
        get_user = User.filter(cursor, username=username)[0]
    except IndexError:
        print("User doas not exist.")
        return None

    if clcrypto.check_password(password, get_user.hashed_password) is False:
        print("This password is incorrect.")
        return None

    get_user.delete(cursor)
    print("User has been delated")


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
        print("Help message: \n")

        print("     -l  Display all available users \n")

        print("     -u & -p  Create a new user e.g.")
        print("     python3 main.py -u franek12 -p tajne123 \n\n")

        print("     -u & -p & -e & -n Change user password e.g.")
        print("     python3 main.py -u franek12 -p tajne123 -e -n tajne1234\n\n")

        print("     -u & -p & -d Delete user from database.")
        print("     python3 main.py -u franek12 -p tajne1234 -d")

    connection.close()

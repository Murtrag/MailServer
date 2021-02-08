#!/usr/local/bin/python3
import sys
import clcrypto

from models import Message
from models import User
from database import get_connection, get_cursor, domain_name

sys.path.append("..")

connection = get_connection()
cursor = get_cursor(connection)
user = User()


def get_messages(username, password):
    try:
        hash_u = user.filter(cursor, username=username)[0].hashed_password
    except IndexError:
        print("User doas not exist.")
        return None

    if clcrypto.check_password(password, hash_u) is False:
        print("This password is incorrect.")
        return None
    return Message.load_received_messages(cursor, f"{username}@{domain_name}")


def send_message(username, password, receiver, t_message):
    try:
        hash_u = user.filter(cursor, username=username)[0].hashed_password
    except IndexError:
        print("User doas not exist.")
        return None

    if clcrypto.check_password(password, hash_u) is False:
        print("This password is incorrect.")
        return None

    if user.filter(cursor, email=receiver) == []:
        print("podany adresat nie instnieje")
        return None

    if bool(t_message) is False:
        print("The flag -s is empty but should privide a text message.")
        return None

    message = Message()

    if "::" in t_message:
        message.title, message.message = t_message.split("::")
    else:
        message.title = "Brak tematu"
        message.message = t_message

    message.sender = user.filter(cursor, username=username)[0].email
    message.receiver = receiver
    message.save_to_db(cursor)
    print("The messages has been sent.")


if __name__ == "__main__":
    if connection is None:
        exit(0)

    pairs = clcrypto.slice_args(sys.argv)
    pairs_keys = pairs.keys()

    if all(param in pairs_keys for param in ("-u", "-p", "-l")):
        """ print all messages of user"""
        # python3 message.py -u franek12 -p tajne1234 -l
        username = pairs["-u"]
        password = pairs["-p"]
        for message in get_messages(username, password):
            print("From: ", message.sender)
            print("Topic: ", message.title)
            print("Message: ", message.message)
            print("-----------------------------\n\n")

    elif all(param in pairs_keys for param in ("-u", "-p", "-t", "-s")):
        """ send message to user """
        # python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::wiadomosc testowa'
        username = pairs["-u"]
        password = pairs["-p"]
        receiver = pairs["-t"]
        message = pairs["-s"]
        send_message(username, password, receiver, message)

    else:
        print("Help message: \n")

        print("-u -p -l Display all user's messages e.g.")
        print("     python3 message.py -u franek12 -p tajne123 -l \n\n")

        print("-u -p -t -s Send message to another user.")
        print(
            " python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::test message \n\n'"
        )

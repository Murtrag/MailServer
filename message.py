from models import Message
from models import User
from database import get_connection, get_cursor, domain_name
import sys
sys.path.append("..")
import clcrypto

connection = get_connection()
cursor = get_cursor(connection)
user = User()

def get_messages(username, password):
    try:
        hash_u = user.load_users_by_any(cursor, username = username)[0].hashed_password
        if clcrypto.check_password(password, hash_u):
            return Message.load_received_messages(cursor, f"{username}@{domain_name}")
        else:
            print("Podano błędne haslo")

    except IndexError:
        print("Podany user nie istnieje")

def send_message(username, password, receiver, t_message):
    hash_u = user.load_users_by_any(cursor, username=username)[0].hashed_password
    if clcrypto.check_password(password, hash_u):
        if user.load_users_by_any(cursor, email=receiver):
            if t_message:
                message = Message()
                message.title = "Brak tematu" if "::" not in t_message else t_message.split("::")[0]
                message.message = t_message if "::"not in t_message else t_message.split("::")[1]
                message.sender = user.load_users_by_any(cursor, username=username)[0].email
                message.receiver = receiver
                message.save_to_db(cursor)
                print("Wiadomość wysłana")
            else:
                print("Brak wiadomości?")
        else:
            print("podany adresat nie instnieje")
    else:
        print("Podano błędne hasło")

if __name__ == '__main__':
    try:
        pairs = clcrypto.slice_args(sys.argv)
    except KeyError as e:
        print(e)
        exit(1)

    if len(set(("-u", "-p", "-l")) & set(pairs)) == 3:
        ''' print all messages of user'''
        # python3 message.py -u franek12 -p tajne1234 -l
        username = pairs['-u']
        password = pairs['-p']
        for message in get_messages(username, password) :
            print("od: ", message.sender)
            print("temat: ", message.title)
            print("treść: ", message.message)
            print("-----------------------------\n\n")

    elif len(set(("-u", "-p", "-t", "-s")) & set(pairs)) == 4:
        ''' send message to user '''
        # python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::wiadomosc testowa'
        username = pairs['-u']
        password = pairs['-p']
        receiver = pairs['-t']
        message = pairs['-s']
        send_message(username, password, receiver, message)


    else:
        print("komunikat pomocy")
        print("-u -p -l Wyświetl wszystkie wiadomości otrzymane przez użytkownika e.g.")
        print("     python3 message.py -u franek12 -p tajne123 -l \n\n")

        print("-u -p -t -s Wyślij wiadomość do innego użytkownika")
        print(" python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::wiadomosc testowa \n\n'")

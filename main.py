from models import User
from database import get_connection, get_cursor
import sys
sys.path.append("..")
import clcrypto

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)


    pairs = clcrypto.slice_args(sys.argv)


    if len(set(("-u","-p")) & set(pairs)) == 2 and len(set(("-e","-d")) & set(pairs)) < 1:
        ''' create user'''
        # python3 main.py -u franek12 -p tajne123
        if User.load_users_by_any(cursor, username=pairs['-u']):
            print("błąd: Taki użytkownik już istnieje ;(")
        elif clcrypto.check_pass_len(pairs['-p']):
            print("Ok tworzymy suera")
            user = User()
            user.username = pairs['-u']
            user.email = pairs['-u']+"@test.pl"
            user.set_password(pairs['-p'],salt="asdf123")
            user.save_to_db(cursor)
        else:
            print("Podane hasło zbyt krótkie")
    elif len(set(("-u","-p", "-e", "-n")) & set(pairs)) == 4:
        ''' change password'''
        # python3 main.py -u franek12 -p tajne123 -e -n tajne1234
        get_user =  User.load_users_by_any(cursor, username=pairs['-u'])[0]
        if get_user:
            if clcrypto.check_password(pairs['-p'], get_user.hashed_password):
                if clcrypto.check_pass_len(pairs['-n']):
                    get_user.set_password(pairs['-n'])
                    get_user.save_to_db(cursor)
                    print("hasło zostało zmienione")
                else:
                    print("Podane hasło jest zbyt słabe")
            else:
                print("podsałeś błędne hasło")
    elif len(set(("-u", "-p", "-d")) & set(pairs)) == 3:
        '''remove user from db'''
        # python3 main.py -u franek12 -p tajne1234 -d
        try:
            get_user = User.load_users_by_any(cursor, username=pairs['-u'])[0]
        except IndexError:
            print("Podany user nie istnieje")
            exit(1)
        if get_user:

            if clcrypto.check_password(pairs['-p'], get_user.hashed_password):
                try:
                    get_user.delete(cursor)
                except Exception:  # psycopg2.IntegrityError
                    print("user nie może być usunięty, poniewaz istnieja wiadomosci do niego przypisane")
                print("usunięto usera z bazy")
            else:
                print("błędne hasło")

    elif set(("-l",)) == set(pairs):
        ''' print all users '''
        # python3 main.py -l
        users = User().load_all_users(cursor)
        print("\n".join([x.username for x in users]))
    else:
        print("komunikat pomocy")

    connection.close()

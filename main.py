from models import User
from database import get_connection, get_cursor
import sys
sys.path.append("..")
import clcrypto

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)

    # user = User()
    # user.username = 'Janusz'
    # user.email = 'janusz@asd.pl'
    # user.set_password('tajne123')
    # user.save_to_db(cursor)
    # user = User.load_user_by_id(cursor, 1)
    # print(user.username)
    # users = User.load_all_users(cursor)
    # print(users)
    #print(User.load_users_by_any(cursor, id=1))
    # print(sys.argv)
    pairs = {}
    for pair_item in sys.argv:
        if "-" in pair_item:
            f_pair_item = pair_item if not "--" in pair_item else pair_item[1:3]
            pairs[f_pair_item] = sys.argv[sys.argv.index(pair_item)+1 : sys.argv.index(pair_item)+2][0]

    if len(set(("-u","-p")) & set(pairs)) == 2 and len(set(("-e","-d")) & set(pairs)) < 1:
        ''' create user'''
        if User.load_users_by_any(cursor, username=pairs['-u']):
            print("błąd: Taki użytkownik już istnieje ;(")
        else:
            print("Ok tworzymy suera")
            user = User()
            user.username = pairs['-u']
            user.email = pairs['-u']+"@test.pl"
            user.set_password(pairs['-p'],salt="asdf123")
            user.save_to_db(cursor)
    elif len(set(("-u","-p", "-e", "-n")) & set(pairs)) == 4:
        ''' change password'''
        get_user =  User.load_users_by_any(cursor, username=pairs['-u'])[0]
        if get_user:
            if clcrypto.check_password(pairs['-p'], get_user.hashed_password):
                get_user.set_password(pairs['-n'])
                get_user.save_to_db(cursor)
                # @TODO check if password has more than 8 chars
                print("hasło zostało zmienione")
            else:
                print("podsałeś błędne hasło")
    elif len(set(("-u", "-p", "-d")) & set(pairs)) == 3:
        get_user = User.load_users_by_any(cursor, username=pairs['-u'])[0]
        # @todo got IndexError: ListIndexOutOfRange if user doesn't exist in database
        if get_user:
            if clcrypto.check_password(pairs['-p'], get_user.hashed_password):
                get_user.delete(cursor)
                print("usunięto usera z bazy")
            else:
                print("błędne hasło")
        else:
            print("Podany user nie istnieje")

    connection.close()

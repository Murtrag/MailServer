# CREATE TABLE users (
#   id serial NOT NULL,
#   username VARCHAR(255) NOT NULL,
#   email VARCHAR(255) UNIQUE NOT NULL,
#   hashed_password VARCHAR(255) NOT NULL,
#   PRIMARY KEY (id)
# );

# CREATE TABLE messages (
# id serial NOT NULL,
# title VARCHAR(255) NOT NULL,
# message TEXT NOT NULL,
# sender VARCHAR(255) NOT NULL,
# receiver VARCHAR(255) NOT NULL,
# creation_date timestamp,
# PRIMARY KEY (id),
# FOREIGN KEY(sender) REFERENCES users(email),
# FOREIGN KEY(receiver) REFERENCES users(email)
# );

# insert into messages(title, message, sender, receiver) values('testowa','tralala', 'Janek123@test.pl', 'Januszek@test.pl');


class Message:
    def __init__(self):
        self.__id = -1
        self.title = ""
        self.message = ""
        self.sender = ""
        self.receiver = ""

    @property
    def id(self):
        return self.__id

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO messages(title, message, sender, receiver)
                     VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.title, self.message, self.sender, self.receiver)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()["id"]
            return True

    @staticmethod
    def load_received_messages(cursor, receiver):
        sql = """SELECT id, sender, title, message FROM messages where receiver=%s ORDER BY creation_date;"""

        cursor.execute(sql, (receiver,))
        ret = []
        for message in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = message["id"]
            loaded_message.title = message["title"]
            loaded_message.message = message["message"]
            loaded_message.sender = message["sender"]
            ret.append(loaded_message)
        return ret

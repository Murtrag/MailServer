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

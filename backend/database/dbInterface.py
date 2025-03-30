import sqlite3

from injector import singleton

from user import user

@singleton
class DatabaseInterface:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.create_table('user/userTable.sql')

    def create_table(self,path):
        with open(path,'r') as file:
            sql_script = file.read()
        self.cursor.execute(sql_script)

    def insertingUser(self,userInfo:user):
        name = userInfo.name
        username = userInfo.username
        password = userInfo.password
        lucky_seed = userInfo.lucky_seed
        self.cursor.execute("insert into users (name, username, password, lucky_seed) values (?,?,?,?)",(name,username,password,lucky_seed))

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        data = self.cursor.fetchone()[3]
        if password == data:
            return True
        else:
            return False
import sqlite3
import time

from injector import singleton

from user import user

@singleton
class DatabaseInterface:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        table_exists = self.cursor.fetchone() is not None
        if not table_exists:
            with open('user/userTable.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.execute(sql_script)

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='blacklist'")
        blacklist_table_exists = self.cursor.fetchone() is not None
        if not blacklist_table_exists:
            with open('blacklist/blacklist.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.execute(sql_script)

        self.cursor.close()
        self.connection.close()

    def insertingUser(self, userInfo: user):
        retry_count = 0
        max_retries = 10

        while retry_count < max_retries:
            try:
                connection = sqlite3.connect('database.db', timeout=10.0)  # Add timeout
                cursor = connection.cursor()
                name = userInfo.name
                username = userInfo.username
                password = userInfo.password
                lucky_seed = userInfo.lucky_seed
                cursor.execute("INSERT INTO user (name, username, password, lucky_seed) VALUES (?,?,?,?)",
                               (name, username, password, lucky_seed))
                connection.commit()
                cursor.close()
                connection.close()
                return True
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and retry_count < max_retries - 1:
                    retry_count += 1
                    time.sleep(0.5)
                    continue
                print(f"Database error after {retry_count} retries: {e}")
                return False
            except sqlite3.IntegrityError:
                return False
            except Exception as e:
                print(f"Error inserting user: {e}")
                return False

    def login(self, username, password):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def addToBlacklist(self, jwt):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO blacklist (jwt) VALUES (?)", (jwt,))
        connection.commit()
        cursor.close()
        connection.close()
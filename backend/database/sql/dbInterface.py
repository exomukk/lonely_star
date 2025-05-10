import sqlite3
import time
import json
from datetime import datetime,timedelta
from Geocoder.geocoderInterface import geocoderInterface
from bcryptService.bcryptService import BcryptService
from user.user import User
from injector import singleton

from user import user

@singleton
class DatabaseInterface:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.geocoderInterface = geocoderInterface()
        with open("database/sql/darkweb2017_top-1000.txt","r") as file:
            self.password_list = file.readlines()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        table_exists = self.cursor.fetchone() is not None
        if not table_exists:
            with open(r'user\userTable.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='blacklist'")
        blacklist_table_exists = self.cursor.fetchone() is not None
        if not blacklist_table_exists:
            with open('blacklist/blacklist.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='upgraderoom'")
        blacklist_table_exists = self.cursor.fetchone() is not None
        if not blacklist_table_exists:
            with open('upgradeSkin/upgradeRecord.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='upgraderoom'")
        blacklist_table_exists = self.cursor.fetchone() is not None
        if not blacklist_table_exists:
            with open('upgradeSkin/upgradeRecord.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='request_logs'")
        blacklist_table_exists = self.cursor.fetchone() is not None
        if not blacklist_table_exists:
            with open('database/sql/requestLogs.sql', 'r') as file:
                sql_script = file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        self.cursor.close()
        self.connection.close()

    def addToBlacklist(self,jwt):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO blacklist (jwt) VALUES (?)", (jwt,))
        connection.commit()
        cursor.close()
        connection.close()

    def checkIfBlacklisted(self,jwt):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blacklist WHERE blacklist = ?", (jwt,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def getUpgradeRecord(self,userID):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM upgraderoom WHERE userID = ?", (userID,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def addUpgradeRecord(self,userID, userWeaponID, expectedWeaponID, successRate, upgradeRate, upgradeDate, success):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO upgraderoom (userID,userWeaponID,expectedWeaponID,successRate,upgradeDate,success) VALUES ( ?,?,?,?,?,?)",
            (userID, userWeaponID, expectedWeaponID, successRate, upgradeRate, upgradeDate, success))
        connection.commit()
        cursor.close()
        connection.close()

    def getLuckySeed(self,id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT lucky_seed FROM user WHERE id = ?", (id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is not None:
            return result[0]
        else:
            return None

    def addCash(self,userID, amount):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE user SET cash = cash + ? WHERE id = ?", (amount, userID))
        connection.commit()
        cursor.close()
        connection.close()

    def getCash(self,userID):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT cash FROM user WHERE id = ?", (userID,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is not None:
            return result[0]
        else:
            return None

    def login(self, username, password):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT id, password, name, username, lucky_seed, cash FROM user WHERE username = ?",(username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is None:
            return False
        stored_pass = result["password"]
        bcrypt_service = BcryptService()
        if bcrypt_service.check_password(password, stored_pass):
            return True
        else:
            return False

    def insertingUser(self, userInfo: User):
        retry_count = 0
        max_retries = 10
        bcrypt_service = BcryptService()
        while retry_count < max_retries:
            try:
                connection = sqlite3.connect('database.db', timeout=10.0)
                cursor = connection.cursor()
                if self.check_pass_in_dictionary(str(userInfo.password) + "\n"):
                    return False
                hashed_password = bcrypt_service.hash_password(userInfo.password)
                cursor.execute(
                    "INSERT INTO user (id, name, username, password, lucky_seed, cash) VALUES (?, ?, ?, ?, ?, 0.00)",
                    (userInfo.id, userInfo.name, userInfo.username, hashed_password, userInfo.lucky_seed))
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
        return None

    def check_pass_in_dictionary(self,password):
        return password in self.password_list

    def add_request_log(self,user_id,request_url,ip_address,geo_location,city):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO request_logs (user_id, request_url, ip_address, geo_location, city) VALUES (?, ?, ?, ?, ?)",
            (user_id, request_url, ip_address, geo_location, city))
        connection.commit()
        cursor.close()
        connection.close()

    def check_abnormal_request(self, ip, user_id, request_url):
        now = datetime.utcnow()
        one_minute_ago = now - timedelta(seconds=60)
        geo_location = self.geocoderInterface.get_location_from_ip(ip)
        geo_location_str = json.dumps(geo_location)

        connection = sqlite3.connect('database.db', timeout=10.0)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT COUNT(*) AS cnt
                          FROM request_logs
                          WHERE ip_address = ?
                            AND user_id = ?
                            AND request_url = ?
                            AND geo_location = ?
                            AND created_at >= ?""",
                       (ip, user_id, request_url, geo_location_str, one_minute_ago))
        row = cursor.fetchone()
        same_hit_count = row["cnt"] if row else 0

        if same_hit_count >= 10:
            cursor.close()
            connection.close()
            return True

        cursor.execute("""SELECT COUNT(DISTINCT geo_location) AS loc_count
                          FROM request_logs
                          WHERE ip_address = ?
                            AND user_id = ?
                            AND created_at >= ?""",
                       (ip, user_id, one_minute_ago))
        row = cursor.fetchone()
        distinct_locs = row["loc_count"] if row else 1

        cursor.close()
        connection.close()

        if distinct_locs > 1:
            return True

        return False

    def getUserIdByUsername(self, username):
        import sqlite3
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is None:
            return None
        return result["id"]

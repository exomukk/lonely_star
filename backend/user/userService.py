from database.sql.dbInterface import DatabaseInterface
from random_heuristic import randomInterface
from user.user import User
import re
class userService():
    def __init__(self):
        self.database = DatabaseInterface()
        self.randomTool = randomInterface
        pass
    def login(self, username, password):
        if DatabaseInterface.login(username, password):
            return True
        else:
            return False
    def register(self, name, username, password, lucky_seed):
        if self.check_password(password):
            user_temp = User(name, username, password, lucky_seed)
            if self.database.insertingUser(user_temp):
                return True
            else:
                return False
        else:
            return False

    def getLuckySeedByID(self, id):
        return self.database.getLuckySeed(id)

    def addCash(self,userID, amount):
        try:
            self.database.addCash(userID, amount)
            return True
        except:
            return False
    def getCash(self, userID):
        return self.database.getCash(userID)

    def check_password(self,password):
        errors = []

        if len(password) < 8:
            errors.append("Must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            errors.append("Must include at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            errors.append("Must include at least one lowercase letter.")
        if not re.search(r"\d", password):
            errors.append("Must include at least one digit.")
        if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]", password):
            errors.append("Must include at least one special character.")

        return len(errors) == 0
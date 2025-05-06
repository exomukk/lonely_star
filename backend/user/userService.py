from database.sql.dbInterface import DatabaseInterface
from random_heuristic import randomInterface
from user.user import User
class userService():
    def __init__(self):
        self.database = DatabaseInterface()
        self.randomTool = randomInterface
        pass
    def login(self, username, password):
        if self.database.login(username, password):
            return True
        else:
            return False
    def register(self, name, username, password, lucky_seed):
        user_temp = User(name, username, password, lucky_seed,0)
        if DatabaseInterface.insertingUser(user_temp):
            return True
        else:
            return False

    def getLuckySeedByID(self, id):
        return DatabaseInterface.getLuckySeed(id)

    def addCash(self,userID, amount):
        try:
            DatabaseInterface.addCash(userID, amount)
            return True
        except:
            return False
    def getCash(self, userID):
        return DatabaseInterface.getCash(userID)
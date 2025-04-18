from injector import inject, singleton, Injector
from database.dbInterface import DatabaseInterface
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
        user_temp = User(name, username, password, lucky_seed)
        if self.database.insertingUser(user_temp):
            return True
        else:
            return False
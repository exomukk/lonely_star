from injector import inject, singleton, Injector
from database.dbInterface import DatabaseInterface
from random_heuristic import randomInterface
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

import json
from flask_jwt_extended import create_access_token

from user.userService import userService
from random_heuristic import randomInterface


class userController:
    def __init__(self):
        self.userService = userService()
        self.randomTool = randomInterface.randomInterface()
        pass


    def login(self, inputs):
        input_loaded = json.loads(inputs)
        username = input_loaded['username']
        password = input_loaded['password']
        if self.userService.login(username,password):
            jwt = create_access_token(identity=username)
            return {
                'status': 'success',
                'jwt': jwt
            },jwt
        else:
            return {'status': 'error', 'message': 'Invalid username or password'}

    def register(self, inputs):
        try:
            input_loaded = json.loads(inputs)
            name = input_loaded['name']
            username = input_loaded['username']
            password = input_loaded['password']
            lucky_seed = self.randomTool.pseudo_random()
            if self.userService.register(name, username, password, lucky_seed):
                return {'status': 'success'}
            else:
                return {'status': 'error', 'message': 'User already exists'}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON data"}



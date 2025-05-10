import json
from flask import jsonify, make_response
from datetime import timedelta
from flask_jwt_extended import create_access_token
from database.sql.dbInterface import DatabaseInterface
from user.userService import userService
from random_heuristic import randomInterface


class userController:
    def __init__(self):
        self.userService = userService()
        self.randomTool = randomInterface.randomInterface()
        self.databaseInterface = DatabaseInterface()

    def login(self, inputs):
        input_loaded = json.loads(inputs)
        username = input_loaded['username']
        password = input_loaded['password']
        user_id = self.userService.login(username, password)
        role = self.databaseInterface.getUserRole(user_id)
        print("role"+role)
        if user_id:
            access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=1),additional_claims={"role": role})
            print(f"[LOGIN] ID: {user_id} | Username: {username} | JWT Token: {access_token}")
            return {'status': 'success'}, access_token
        else:
            return {'status': 'error', 'message': 'Invalid username or password'}, None

    def register(self, inputs):
        try:
            print("register input from client: ", inputs)
            # input_loaded = json.loads(inputs)
            input_loaded = inputs
            name = input_loaded['name']
            username = input_loaded['username']
            password = input_loaded['password']
            lucky_seed = self.randomTool.pseudo_random()
            print("register input from client 2: ", name, username, password, lucky_seed)
            # print("register response: ", self.userService.register(name, username, password, lucky_seed))
            if self.userService.register(name, username, password, lucky_seed):
                access_token = create_access_token(identity=name, expires_delta=timedelta(hours=1))
                print("access token: ", access_token)
                print(f"[REGISTER] ID: {name} | Username: {username} | JWT Token: {access_token}")
                return {'status': 'success'}, access_token
            else:
                return {'status': 'error', 'message': 'User already exists'}, None

        except Exception as e:
            print("[REGISTER] Exception:", e)
            return {"status": "error", "message": "Invalid data"}, None



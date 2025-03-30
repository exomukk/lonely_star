import json

import app
from user.userService import userService
from flask import jsonify

from random_heuristic import randomInterface


class userController:
    def __init__(self):
        self.userService = userService()
        self.randomTool = randomInterface
        pass
    @app.route('/login', methods=['POST'])
    def login(self,input):
        input = json.loads(input)
        username = input['username']
        password = input['password']
        if self.userService.login(username,password):
            session = self.randomTool.randomInterface.pseudo_random()
            return jsonify({
                'status': 'success',
                'session': session
            })
        else:
            return {'status': 'error', 'message': 'Invalid username or password'}


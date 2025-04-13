from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended import set_access_cookies
from flask_socketio import SocketIO
app = Flask(__name__)

# Use CORS temporary for development

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

#Websocket configuration
#socket = SocketIO(app,cors_allowed_origins="http://localhost:3000")

# Future configuration for production

# Services importation
#socketService = socketServiceInterface.SocketService()

#import socket.socketController as socketControllerInterface
#socketController = socketControllerInterface.SocketController(socket, socketService)

import user.userController as userControllerInterface
userController = userControllerInterface.userController()

import random_heuristic.randomInterface as randomInterface
randomTool = randomInterface.randomInterface()

#JWT configurations
app.config['SECRET_KEY'] = randomTool.pseudo_random()
app.config["JWT_SECRET_KEY"] = randomTool.pseudo_random()
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

#Route configuration
@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"

@app.route('/register', methods=['POST'])
def register():
    inputs = request.data.decode('utf-8')
    return jsonify(userController.register(inputs))

@app.route('/login', methods=['POST'])
def login():
    inputs = request.data.decode('utf-8')
    login_info = userController.login(inputs)
    json_output = jsonify(login_info[0])
    set_access_cookies(json_output,login_info[1])
    return json_output


if __name__ == '__main__':
    app.run()

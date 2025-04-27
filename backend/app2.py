from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from flask_jwt_extended import set_access_cookies
from flask_socketio import SocketIO

# Thêm import
from gun.gun_routes import gun_bp

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Các phần websocket, userController, randomTool...
import user.userController as userControllerInterface
userController = userControllerInterface.userController()

import random_heuristic.randomInterface as randomInterface
randomTool = randomInterface.randomInterface()

app.config['SECRET_KEY'] = randomTool.pseudo_random()
app.config["JWT_SECRET_KEY"] = randomTool.pseudo_random()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

# Thêm đăng ký blueprint gun
app.register_blueprint(gun_bp)

# Các route / /index /home /me /register /login /logout ...
@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"

@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify({
        'status': 'success',
        'username': current_user,
    }), 200

@app.route('/register', methods=['POST'])
def register():
    inputs = request.data.decode('utf-8')
    return jsonify(userController.register(inputs))

@app.route('/login', methods=['POST'])
def login():
    inputs = request.data.decode('utf-8')
    login_info, jwt_token = userController.login(inputs)
    json_output = jsonify(login_info)
    if jwt_token:
        set_access_cookies(json_output, jwt_token)
    return json_output

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'status': 'success', 'message': 'Đăng xuất thành công'})
    unset_jwt_cookies(response)
    return response, 200

if __name__ == '__main__':
    app.run()

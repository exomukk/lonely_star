from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies
from flask_jwt_extended import set_access_cookies
# from flask_socketio import SocketIO

# Thêm import Blueprint
from gun.gun_routes import gun_bp
from chest.chest_routes import chest_bp
from inventory.inventory_routes import inventory_bp
# (sau này thêm inventory/inventory_routes import inventory_bp nếu có)

app = Flask(__name__)

# Use CORS temporary for development
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# WebSocket configuration (tạm comment)
# socket = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Future configuration for production
# socketService = socketServiceInterface.SocketService()
# socketController = socketControllerInterface.SocketController(socket, socketService)

# Các phần websocket, userController, randomTool...
import user.userController as userControllerInterface
userController = userControllerInterface.userController()

import random_heuristic.randomInterface as randomInterface
randomTool = randomInterface.randomInterface()

# JWT configurations
app.config['SECRET_KEY'] = randomTool.pseudo_random()
app.config["JWT_SECRET_KEY"] = randomTool.pseudo_random()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)

# Route Blueprint configuration
app.register_blueprint(gun_bp)
app.register_blueprint(chest_bp)
app.register_blueprint(inventory_bp)
# app.register_blueprint(inventory_bp)  # <- sau này inventory xong thì thêm

# Các route basic: / /index /home /me /register /login /logout
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

# Importing required libraries and modules
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt, \
    create_access_token
from flask_jwt_extended import set_access_cookies
from upgradeSkin.upgradeService import upgradeRoomService
from datetime import timedelta
from database.sql.dbInterface import DatabaseInterface as db
DatabaseInterface = db()
from database.sql.requestLoggerInterface import requestLoggerInterface
from werkzeug.middleware.proxy_fix import ProxyFix
import user.userController as userControllerInterface
userController = userControllerInterface.userController()
import random_heuristic.randomInterface as randomInterface
randomTool = randomInterface.randomInterface()
from gun.gun_service import GunService
from inventory.inventory_service import sell_item_from_inventory
from chest.chest_service import get_all_chests, get_chest_by_id, random_rarity
from inventory.inventory_service import (get_inventory,add_item_to_inventory,check_item_executing,change_item_executing)
from otp.otp_service import otp_service
gun_service = GunService()
app = Flask(__name__)

app.otp_service = otp_service

# Middleware to handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Load environment variables
load_dotenv()
ssl_context_str = os.getenv("SSL_CONTEXT")
if ssl_context_str:
    context = eval(ssl_context_str)
else:
    context = None

app.config["SSL_CONTEXT"] = context

# Use CORS temporary for development
CORS(app, origins=["http://localhost:3000","https://scamclub.creammjnk.uk"], supports_credentials=True)

# JWT configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config['SECRET_KEY'] = randomTool.pseudo_random()
app.config["JWT_SECRET_KEY"] = randomTool.pseudo_random()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)


# Flask mail configuration

app.config.update({
    "MAIL_SERVER":   "smtp.gmail.com",
    "MAIL_PORT":     587,
    "MAIL_USE_TLS":  True,
    "MAIL_USERNAME": "wdev2616@gmail.com",
    "MAIL_PASSWORD": "xrqa voxy uwbs jffx",
    "MAIL_DEFAULT_SENDER": ("WebDev", "wdev2616@gmail.com")
})
mail = Mail(app)
from otp.routes import otp_bp
app.register_blueprint(otp_bp)


# Main pages and functions routes
@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"

@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    print('[DEBUG] me: ', current_user)
    return jsonify({
        'status': 'success',
        'username': current_user,
    }), 200

@app.route('/check', methods=['GET'])
def check():
    return jsonify({
        'status': 'success',
        'message': 'Server is running properly'
    }), 200

@app.route('/register', methods=['POST'])
# check ip
def register():
    data = request.get_json(silent=True) or {}

    result, access_token = userController.register(data)
    print(result, " ", access_token)
    print("[REGISTER] result:", result)

    if result.get('status') == 'success':
    # if result.get('status') == 'error':
        # For debug
        email = data.get('username').strip().lower()
        otp_code = otp_service.generate_otp()
        otp_service.store_otp(email, otp_code)
        print("[REGISTER] otp_store sau khi store:", otp_service.otp_store)

        try:
            otp_service.send_otp_mail(email, otp_code)
            print(f"OTP {otp_code} sent to {email}")
            result["otp_sent"] = True
        except Exception as e:
            print(f"Failed to send OTP to {email}: {e}")
            result["otp_sent"] = False

        # Trả về response có set JWT cookie
        response = jsonify(result)
        print('[REGISTER] response:', response)
        if access_token:
            set_access_cookies(response, access_token)
        return response

    return jsonify(result)


@app.route('/login', methods=['POST'])
def login():
    inputs = request.data.decode('utf-8')
    login_info, jwt_token = userController.login(inputs)
    json_output = jsonify(login_info)
    if jwt_token:
        set_access_cookies(json_output, jwt_token)
    return json_output

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    DatabaseInterface.addToBlacklist(get_jwt()['jti'])
    response = jsonify({'status': 'success', 'message': 'Đăng xuất thành công'})
    unset_jwt_cookies(response)
    return response, 200


#Gun Routes

@app.route('/api/gun/search', methods=['GET'])
def api_search_gun():
    query = request.args.get('q', '')
    result = [g.to_dict() for g in gun_service.search_by_name_or_price(query)]
    return jsonify(result)

@app.route('/api/gun/price_range', methods=['GET'])
def api_gun_by_price():
    min_price = float(request.args.get('min', 0))
    max_price = float(request.args.get('max', 9999))
    result = [g.to_dict() for g in gun_service.get_by_price_range(min_price, max_price)]
    return jsonify(result)

@app.route('/api/gun/<gun_id>', methods=['GET'])
def api_get_gun_by_id(gun_id):
    skin = gun_service.get_skin_by_id(gun_id)
    if skin:
        return jsonify(skin)
    return jsonify({'error': 'not found'}), 404

# Chest Routes
@app.route('/api/chests', methods=['GET'])
def api_get_chests():
    chests = get_all_chests()
    for chest in chests:
        chest['_id'] = str(chest['_id'])
    return jsonify(chests), 200

@app.route('/api/open_chest', methods=['POST'])
@jwt_required()
def api_open_chest():
    data = request.get_json()
    chest_id = data.get('chest_id')
    if not chest_id:
        return jsonify({'error': 'chest_id is required'}), 400

    chest_info = get_chest_by_id(chest_id)
    if not chest_info:
        return jsonify({'error': 'Chest not found'}), 404

    selected_rarity = random_rarity(chest_info)
    skin = gun_service.get_skin_by_rarity(selected_rarity)

    user_id = get_jwt_identity()
    add_item_to_inventory(user_id, skin['id'], chest_id)

    return jsonify({
        'message': 'Chest opened successfully',
        'skin': skin,
        'rarity': selected_rarity
    }), 200

# Inventory Routes
@app.route('/api/inventory', methods=['GET'])
@jwt_required()
def api_get_inventory():
    user_id = get_jwt_identity()
    items = get_inventory(user_id)
    return jsonify({
        "status": "success",
        "inventory": items
    }), 200

@app.route('/api/item_state/<skin_id>', methods=['GET'])
@jwt_required()
def api_check_item_state(skin_id):
    user_id = get_jwt_identity()
    state = check_item_executing(user_id, skin_id)
    return jsonify({
        "skin_id": skin_id,
        "isExecuting": state
    })

@app.route('/api/item_state/<skin_id>', methods=['POST'])
@jwt_required()
def api_change_item_state(skin_id):
    user_id = get_jwt_identity()
    new_state = request.json.get("isExecuting", False)
    change_item_executing(user_id, skin_id, new_state)
    return jsonify({
        "skin_id": skin_id,
        "newState": new_state
    }), 200

@app.route('/api/sell_skin', methods=['POST'])
@jwt_required()
def api_sell_skin():
    user_id = get_jwt_identity()
    data = request.get_json()
    skin_id = data.get("skin_id")

    if not skin_id:
        return jsonify({"success": False, "message": "skin_id is required"}), 400

    result = sell_item_from_inventory(user_id, skin_id)

    if result["success"]:
        return jsonify({
            "success": True,
            "message": f"Sold skin {skin_id} for {result['value']}$",
            "earned": result["value"]
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": result["reason"]
        }), 400

@app.route('/api/rollRate', methods=['GET'])
@jwt_required()
def rollRate():
    user_id = get_jwt_identity()
    userWeaponID = request.args.get('userWeaponID')
    expectedWeaponID = request.args.get('expectedWeaponID')

    if not userWeaponID or not expectedWeaponID:
        return jsonify({"error": "userWeaponID and expectedWeaponID are required"}), 400

    rate = upgradeRoomService.rollRate(user_id, userWeaponID, expectedWeaponID)
    return jsonify({"rate": rate}), 200

@app.route('/api/upgradeSkin', methods=['POST'])
@jwt_required()
def upgradeSkin():
    user_id = get_jwt_identity()
    data = request.get_json()
    userWeaponID = data.get('userWeaponID')
    expectedWeaponID = data.get('expectedWeaponID')
    startRange = data.get('startRange')
    endRange = data.get('endRange')

    if not userWeaponID or not expectedWeaponID:
        return jsonify({"error": "userWeaponID and expectedWeaponID are required"}), 400

    result = upgradeRoomService.executeRoll(user_id, userWeaponID, expectedWeaponID, startRange, endRange)
    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 500

@app.route('/api/currentCash', methods=['GET'])
@jwt_required()
def getCurrentCash():
    user_id = get_jwt_identity()
    cash = userController.userService.getCash(user_id)
    if cash is not None:
        return jsonify({"cash": cash}), 200
    else:
        return jsonify({"error": "User not found"}), 404


# Security Configuration


request_logger = requestLoggerInterface()

@app.before_request
def check_request():
    ip = request.remote_addr
    try:
        user_id = get_jwt_identity()
    except Exception:
        user_id = None

    # if request_logger.check_abnormal_request(ip, user_id, request.url):
    #     return jsonify({'error': 'Too many requests'}), 429

@app.after_request
def strip_server_header(response):
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)
    response.headers.pop('X-AspNet-Version', None)
    return response

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    db = DatabaseInterface
    token_in_blocklist = db.checkIfBlacklisted(jti)
    return token_in_blocklist

if __name__ == '__main__':
    app.run(ssl_context=context)

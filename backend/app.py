# Importing required libraries and modules
from random import random, choice
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt
# from database.sql.dbInterface import DatabaseInterface
from flask_jwt_extended import set_access_cookies
from upgradeSkin.upgradeService import upgradeRoomService as upgradeService
upgradeService = upgradeService()
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
from server_performance.server_performance_interface import server_performance_interface
server_performance = server_performance_interface()
app = Flask(__name__)

app.otp_service = otp_service

# Middleware to handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# Load environment variables
load_dotenv()
ssl_context_str = os.getenv("SSL_CONTEXT")
admin_account = str(os.getenv("ADMIN_ACCOUNT"))
admin_password = str(os.getenv("ADMIN_PASSWORD"))


# Set up SSL context
if ssl_context_str:
    context = eval(ssl_context_str)
else:
    context = None
app.config["SSL_CONTEXT"] = context

# Setup admin account
databaseInterface = DatabaseInterface
if admin_account and admin_password:
    created = databaseInterface.createAdminAccount(admin_account, admin_password)
else:
    print("Missing ADMIN_ACCOUNT or ADMIN_PASSWORD environment variable.")

# Use CORS temporary for development
CORS(app, origins=["http://localhost:3000","https://scamclub.creammjnk.uk"], supports_credentials=True)

# JWT configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['headers','cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # Không fix được khi logout :(
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
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
    claims = get_jwt()
    user_name = claims.get("name")
    print('[DEBUG] me: ', user_name)
    print('[DEBUG] me: ', current_user)
    return jsonify({
        'status': 'success',
        'username': user_name,
    }), 200

@app.route('/api/check', methods=['GET'])
@jwt_required()
def check():
    claims = get_jwt()
    print(claims.get("role"))
    if claims.get("role") != "admin":
        return jsonify({"error": "Access forbidden: Admins only"}), 403
    return jsonify({
        'status': 'success',
        'message': 'Server is running properly',
        'CPU Usage': server_performance.get_cpu_usage(),
        'Memory Usage': server_performance.get_memory_usage()
    }), 200

@app.route('/api/is_admin', methods=['GET'])
@jwt_required()
def is_admin():
    claims = get_jwt()
    print(claims.get("role"))
    if claims.get("role") != "admin":
        return jsonify({"admin": "false"}), 200
    return jsonify({"admin": "true"}), 200

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
    print("[LOGOUT] JWT): ", get_jwt()['jti'])
    DatabaseInterface.addToBlacklist(get_jwt()['jti'])
    response = jsonify({'status': 'success', 'message': 'Đăng xuất thành công'})
    unset_jwt_cookies(response)
    return response, 200


#Gun Routes

@app.route('/api/gun/search', methods=['POST'])
def api_search_gun():
    data = request.get_json() or {}
    query = data.get('q', '')
    result = [g.to_dict() for g in gun_service.search_by_name(query)]
    return jsonify(result)


@app.route('/api/gun/price_range', methods=['POST'])
def api_gun_by_price_range():
    data = request.get_json() or {}
    print('api_gun_by_price is running: ', data)

    try:
        base_price = float(data.get('base_price'))
        multiplier = float(data.get('multiplier'))
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Missing or invalid data"}), 400

    target_price = base_price * multiplier
    delta = target_price * 0.1
    min_price = round(target_price - delta, 2)
    max_price = round(target_price + delta, 2)

    print(f"[DEBUG] base={base_price}, multiplier={multiplier}, target={target_price}, range=({min_price}, {max_price})")

    guns = [g.to_dict() for g in gun_service.guns if min_price <= g.price <= max_price]

    return jsonify({
        "status": "success",
        "target_price": target_price,
        "range": [min_price, max_price],
        "count": len(guns),
        "guns": guns
    }), 200

@app.route('/api/gun/<gun_id>', methods=['GET'])
def api_get_gun_by_id(gun_id):
    skin = gun_service.get_skin_by_id(gun_id)
    if skin:
        return jsonify(skin)
    return jsonify({'error': 'not found'}), 404

#Temp route for testing
@app.route('/api/gun/by_id', methods=['POST'])
def api_get_gun_by_id_post():
    data = request.get_json() or {}
    skin_id = data.get("id")

    if skin_id is None:
        return jsonify({"status": "error", "message": "Missing 'id' in request"}), 400

    skin = gun_service.get_skin_by_id(skin_id)
    if skin:
        return jsonify({
            "status": "success",
            "skin": skin,
            "price": skin["price"]
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": f"Skin with id {skin_id} not found"
        }), 404

@app.route('/api/gun/list_by_rarity', methods=['POST'])
def api_list_guns_by_rarity():
    data = request.get_json() or {}
    rarity = data.get("rarity")

    if not rarity:
        return jsonify({"status": "error", "message": "Missing 'rarity' in request"}), 400

    filtered_guns = [
        gun.to_dict() for gun in gun_service.guns
        if gun.tierlist.lower() == rarity.lower()
    ]

    if not filtered_guns:
        return jsonify({
            "status": "error",
            "message": f"No guns found with rarity '{rarity}'"
        }), 404

    return jsonify({
        "status": "success",
        "rarity": rarity,
        "count": len(filtered_guns),
        "guns": filtered_guns
    }), 200


# Chest Routes
@app.route('/api/chests', methods=['GET'])
def api_get_chests():
    chests = get_all_chests()
    result = []
    for chest in chests:
        data = chest.to_dict()
        data['_id'] = str(data['_id'])  # để đảm bảo JSON hợp lệ
        result.append(data)
    return jsonify(result), 200

@app.route('/api/open_chest', methods=['POST'])
@jwt_required()
def api_open_chest():
    data = request.get_json() or {}
    chest_id = data.get("chest_id")
    user_id = get_jwt_identity()
    print("data when open chest", data, " ", chest_id, " ", user_id)

    if not chest_id:
        return jsonify({"error": "Missing chest_id"}), 400

    chest_info = get_chest_by_id(chest_id)
    print("opening chest", chest_info)
    if not chest_info:
        return jsonify({'error': 'Chest not found'}), 404

    current_cash = userController.userService.getCash(user_id)
    if current_cash is None:
        return jsonify({'error': 'User not found'}), 404

    if hasattr(chest_info, "reward_values") and chest_info.reward_values:
        reward_values = chest_info.reward_values
        print('[DEBUG] reward_values:', reward_values)
        reward = choice(reward_values)
        userController.userService.addCash(user_id, reward)
        return jsonify({
            "message": "Free cash chest opened!",
            "reward": f"${reward}",
            "new_balance": current_cash + reward
        }), 200

    if current_cash < abs(chest_info.price):
        return jsonify({'error': 'Not enough cash to open this chest'}), 400

    userController.userService.addCash(user_id, -chest_info.price)

    selected_rarity = random_rarity(chest_info, user_id)
    skin = gun_service.get_skin_by_rarity(selected_rarity)

    add_item_to_inventory(user_id, skin['id'], chest_id)

    return jsonify({
        'message': 'Chest opened successfully',
        'skin': skin,
        'rarity': selected_rarity,
        'new_balance': current_cash - chest_info.price
    }), 200

@app.route('/api/chest_info/<chest_id>', methods=['GET'])
def get_chest_detail(chest_id):
    chest = get_chest_by_id(chest_id)
    if not chest:
        return jsonify({'error': 'Chest not found'}), 404

    if hasattr(chest, 'reward_values') and chest.reward_values:
        return jsonify({
            'type': 'cash',
            'reward_values': chest.reward_values
        })

    skins = []
    for rarity, percent in chest.rarity_distribution.items():
        # Trả về danh sách skin dạng dict
        rarity_skins = gun_service.get_skins_by_rarity(rarity)
        print("rarity_skins: ", rarity_skins)

        # Đảm bảo mỗi skin là dict
        for skin in rarity_skins:
            if isinstance(skin, dict):
                skins.append({
                    'name': skin.get('name', 'Unknown'),
                    'image': skin.get('image', ''),
                    'rarity': rarity
                })

    return jsonify({
        'type': 'skin',
        'skins': skins
    })


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
    print('RollRate DEBUG: ', user_id, " ", userWeaponID, " ", expectedWeaponID)
    if not userWeaponID or not expectedWeaponID:
        return jsonify({"error": "userWeaponID and expectedWeaponID are required"}), 400

    rate = upgradeService.rollRate(user_id, userWeaponID, expectedWeaponID)
    print("rate: ", rate)
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

    result = upgradeService.executeRoll(user_id, userWeaponID, expectedWeaponID, startRange, endRange)
    if result:
        print("Win upgrade")
        return jsonify({"success": True}), 200
    else:
        print("Lose upgrade")
        return jsonify({"success": False}), 200

@app.route('/api/currentCash', methods=['GET'])
@jwt_required()
def getCurrentCash():
    user_id = get_jwt_identity()
    cash = userController.userService.getCash(user_id)
    if cash is not None:
        return jsonify({"cash": cash}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/skin/<int:skin_id>', methods=['GET'])
@jwt_required()
def get_skin_by_id_route(skin_id):
    skin_data = gun_service.get_skin_by_id(skin_id)
    if skin_data:
        return jsonify(skin_data), 200
    else:
        return jsonify({"error": "Skin not found"}), 404


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
    app.run(ssl_context=context,debug=True)

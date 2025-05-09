from flask import Flask, request, jsonify, g
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required,
    get_jwt_identity, unset_jwt_cookies, get_jwt,
    set_access_cookies
)
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
from upgradeSkin.upgradeService import upgradeRoomService
from database.sql.dbInterface import DatabaseInterface

import time
import user.userController as userControllerInterface
import random_heuristic.randomInterface as randomInterface

# Các service riêng
from gun.gun_service import GunService
from inventory.inventory_service import (
    sell_item_from_inventory,
    get_inventory, add_item_to_inventory,
    check_item_executing, change_item_executing
)
from chest.chest_service import get_all_chests, get_chest_by_id, random_rarity

from otp.otp_service import generate_otp, store_otp, send_otp_mail

# ==== Khởi tạo app ====
app = Flask(__name__)

# Đặt ProxyFix ngay sau khi tạo app
# Nếu deploy sau Nginx/ngrok, sẽ lấy đúng IP gốc trong request.remote_addr
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# CORS (dev)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Cấu hình Flask-Mail
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

# JWT configs
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
# import random
randomTool = randomInterface.randomInterface()
app.config['SECRET_KEY'] = randomTool.pseudo_random()
app.config["JWT_SECRET_KEY"] = randomTool.pseudo_random()
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

jwt = JWTManager(app)

# Khởi tạo controller và service
userController = userControllerInterface.userController()
gun_service = GunService()

# ==== RATE-LIMIT & BAN IP ====
ip_records = {}    # { ip: [timestamp, ...] }
banned_ips = {}    # { ip: ban_end_timestamp }

LIMIT = 10         # 10 requests
WINDOW = 60        # trong 60 giây
BAN_DURATION = 300 # ban 5 phút

@app.before_request
def attach_and_rate_limit():
    # Lấy IP client từ header X-Forwarded-For hoặc request.remote_addr
    forwarded = request.headers.get('X-Forwarded-For')
    ip = (forwarded.split(',')[0].strip() if forwarded else request.remote_addr)
    g.client_ip = ip

    now = time.time()
    # Kiểm tra ban
    ban_until = banned_ips.get(ip)
    if ban_until and now < ban_until:
        return jsonify({
            "error": "Too many requests. You are banned for a while."
        }), 429
    elif ban_until:
        # hết hạn ban
        banned_ips.pop(ip, None)

    # Cập nhật record trong WINDOW
    times = ip_records.get(ip, [])
    times = [t for t in times if now - t < WINDOW]
    times.append(now)
    ip_records[ip] = times

    # Nếu vượt limit → ban
    if len(times) > LIMIT:
        banned_ips[ip] = now + BAN_DURATION
        ip_records.pop(ip, None)
        return jsonify({
            "error": f"Exceeded {LIMIT} requests per {WINDOW}s. "
                     f"Banned for {BAN_DURATION//60} minutes."
        }), 429
    return None


# ==== Các route cơ bản ====
@app.route('/')
@app.route('/index')
@app.route('/home')
def entrypoint():
    return "../main.html"


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    db = DatabaseInterface()
    return db.checkIfBlacklisted(jti)


@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify({
        'status': 'success',
        'username': get_jwt_identity(),
    }), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    # nếu muốn dùng IP: userController.register(data, g.client_ip)
    # gọi controller để tạo user
    result = userController.register(data)
    email = data.get('username')
    otp_code = generate_otp()
    store_otp(email, otp_code)
    try:
        send_otp_mail(email, otp_code)
        print(f"OTP {otp_code} sent to {email}")
    except Exception as e:
        print(f"Failed to send OTP to {email}: {e}")
            # tuỳ chọn: trả về error nếu cần
            # return jsonify({'status':'error','message':'Không gửi được OTP'}), 500
    return jsonify(userController.register(data))


# ==== Route /login đã cập nhật ====
@app.route('/login', methods=['POST'])
def login():
    print('calling login')
    data = request.get_json(silent=True) or {}
    client_ip = g.client_ip

    # Debug payload
    print('DEBUG [login] payload:', { **data, 'client_ip': client_ip })

    # Gọi controller
    login_info, jwt_token = userController.login(data, client_ip)

    # Đính IP vào response
    login_info['client_ip'] = client_ip

    response = jsonify(login_info)
    if jwt_token:
        set_access_cookies(response, jwt_token)
    return response


@app.route('/logout', methods=['POST'])
def logout():
    DatabaseInterface.addToBlacklist(get_jwt()['jti'])
    resp = jsonify({'status': 'success', 'message': 'Đăng xuất thành công'})
    unset_jwt_cookies(resp)
    return resp, 200


# ==== Gun Routes ====
@app.route('/api/gun/search', methods=['GET'])
def api_search_gun():
    query = request.args.get('q', '')
    result = [g.to_dict() for g in gun_service.search_by_name_or_price(query)]
    return jsonify(result)


@app.route('/api/gun/price_range', methods=['GET'])
def api_gun_by_price():
    min_p = float(request.args.get('min', 0))
    max_p = float(request.args.get('max', 9999))
    result = [g.to_dict() for g in gun_service.get_by_price_range(min_p, max_p)]
    return jsonify(result)


@app.route('/api/gun/<gun_id>', methods=['GET'])
def api_get_gun_by_id(gun_id):
    skin = gun_service.get_skin_by_id(gun_id)
    return jsonify(skin) if skin else (jsonify({'error': 'not found'}), 404)


# ==== Chest Routes ====
@app.route('/api/chests', methods=['GET'])
def api_get_chests():
    chests = get_all_chests()
    for chest in chests:
        chest['_id'] = str(chest['_id'])
    return jsonify(chests), 200


@app.route('/api/open_chest/<chest_id>', methods=['POST'])
@jwt_required()
def api_open_chest(chest_id):
    user_id = get_jwt_identity()

    chest_info = get_chest_by_id(chest_id)
    if not chest_info:
        return jsonify({'error': 'Chest not found'}), 404

    current_cash = userController.userService.getCash(user_id)
    if current_cash is None:
        return jsonify({'error': 'User not found'}), 404

    if current_cash < chest_info.price:
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



# ==== Inventory Routes ====
@app.route('/api/inventory', methods=['GET'])
@jwt_required()
def api_get_inventory():
    items = get_inventory(get_jwt_identity())
    return jsonify({"status": "success", "inventory": items}), 200


@app.route('/api/item_state/<skin_id>', methods=['GET'])
@jwt_required()
def api_check_item_state(skin_id):
    return jsonify({
        "skin_id": skin_id,
        "isExecuting": check_item_executing(get_jwt_identity(), skin_id)
    })


@app.route('/api/item_state/<skin_id>', methods=['POST'])
@jwt_required()
def api_change_item_state(skin_id):
    new_state = request.json.get("isExecuting", False)
    change_item_executing(get_jwt_identity(), skin_id, new_state)
    return jsonify({"skin_id": skin_id, "newState": new_state}), 200


@app.route('/api/sell_skin', methods=['POST'])
@jwt_required()
def api_sell_skin():
    data = request.get_json() or {}
    skin_id = data.get("skin_id")
    if not skin_id:
        return jsonify({"success": False, "message": "skin_id is required"}), 400

    result = sell_item_from_inventory(get_jwt_identity(), skin_id)
    if result["success"]:
        return jsonify({
            "success": True,
            "message": f"Sold skin {skin_id} for {result['value']}$",
            "earned": result["value"]
        }), 200
    else:
        return jsonify({"success": False, "message": result["reason"]}), 400


# ==== Upgrade & Roll Routes ====
@app.route('/api/rollRate', methods=['GET'])
@jwt_required()
def rollRate():
    args = request.args
    uid = get_jwt_identity()
    uwid = args.get('userWeaponID')
    ewid = args.get('expectedWeaponID')
    if not uwid or not ewid:
        return jsonify({"error": "userWeaponID and expectedWeaponID are required"}), 400
    return jsonify({"rate": upgradeRoomService.rollRate(uid, uwid, ewid)}), 200


@app.route('/api/upgradeSkin', methods=['POST'])
@jwt_required()
def upgradeSkin():
    data = request.get_json() or {}
    uid = get_jwt_identity()
    uwid = data.get('userWeaponID')
    ewid = data.get('expectedWeaponID')
    sr = data.get('startRange')
    er = data.get('endRange')
    if not uwid or not ewid:
        return jsonify({"error": "userWeaponID and expectedWeaponID are required"}), 400

    success = upgradeRoomService.executeRoll(uid, uwid, ewid, sr, er)
    return jsonify({"success": success}), (200 if success else 500)


@app.route('/api/currentCash', methods=['GET'])
@jwt_required()
def getCurrentCash():
    uid = get_jwt_identity()
    cash = userController.userService.getCash(uid)
    return (jsonify({"cash": cash}), 200) if cash is not None else (jsonify({"error": "User not found"}), 404)


if __name__ == '__main__':
    app.run(ssl_context=('ca_certs/localhost+2.pem', 'ca_certs/localhost+2-key.pem'))

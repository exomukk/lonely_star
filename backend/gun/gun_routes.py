from flask import Blueprint, jsonify
import json
import random
import os

gun_bp = Blueprint('gun', __name__, url_prefix='/gun')

# Load weapons.json
current_dir = os.path.dirname(__file__)
with open(os.path.join(current_dir, 'weapons.json'), 'r', encoding='utf-8') as f:
    weapons = json.load(f)

# API: Lấy tất cả skin
@gun_bp.route('/all', methods=['GET'])
def get_all_weapons():
    return jsonify(weapons)

# API: Random 1 skin
@gun_bp.route('/random', methods=['GET'])
def get_random_weapon():
    weapon_name = random.choice(list(weapons.keys()))
    return jsonify(weapons[weapon_name])

# API: Lấy skin theo tên (không bắt buộc, để sau dùng)
@gun_bp.route('/<weapon_name>', methods=['GET'])
def get_weapon_by_name(weapon_name):
    weapon = weapons.get(weapon_name)
    if weapon:
        return jsonify(weapon)
    else:
        return jsonify({'error': 'Weapon not found'}), 404

from flask import Blueprint, request, jsonify
from chest.chest_service import get_all_chests, get_chest_by_id, random_rarity
from gun.gun_service import get_skin_by_rarity  # lấy skin theo độ hiếm
from inventory.inventory_service import add_item_to_inventory  # thêm vào kho đồ
from flask import session  # hoặc dùng JWT nếu bạn đang xài

chest_bp = Blueprint('chest_bp', __name__)


@chest_bp.route('/api/chests', methods=['GET'])
def api_get_chests():
    """
    API lấy danh sách các hòm
    """
    chests = get_all_chests()
    for chest in chests:
        chest['_id'] = str(chest['_id'])  # ép string cho JSON serialize được
    return jsonify(chests), 200


@chest_bp.route('/api/open_chest', methods=['POST'])
def api_open_chest():
    """
    API mở 1 hòm: random 1 skin theo xác suất của hòm đó
    """
    data = request.get_json()
    chest_id = data.get('chest_id')

    if not chest_id:
        return jsonify({'error': 'chest_id is required'}), 400

    # Lấy thông tin hòm
    chest_info = get_chest_by_id(chest_id)
    if not chest_info:
        return jsonify({'error': 'Chest not found'}), 404

    # Random độ hiếm
    selected_rarity = random_rarity(chest_info)

    # Random 1 skin theo độ hiếm (lấy từ weapons.json)
    skin = get_skin_by_rarity(selected_rarity)

    # Giả sử bạn đang lưu user_id trong session (hoặc JWT decode)
    user_id = session.get('user_id')  # hoặc decode từ token

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    # Thêm skin vào inventory user
    add_item_to_inventory(user_id, skin['id'], chest_id)

    return jsonify({
        'message': 'Chest opened successfully',
        'skin': skin,
        'rarity': selected_rarity
    }), 200

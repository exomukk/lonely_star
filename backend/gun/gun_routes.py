from flask import Blueprint, jsonify, request
from backend.gun.gun_service import GunService

gun_bp = Blueprint('gun', __name__, url_prefix='/gun')

gun_service = GunService()

# API: lấy toàn bộ skin
@gun_bp.route('/all', methods=['GET'])
def get_all_weapons():
    return jsonify([gun.to_dict() for gun in gun_service.guns])

# API: lấy skin theo khoảng giá
@gun_bp.route('/price-range', methods=['GET'])
def get_by_price_range():
    try:
        min_price = float(request.args.get('min'))
        max_price = float(request.args.get('max'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid min or max price'}), 400

    guns = gun_service.get_by_price_range(min_price, max_price)
    return jsonify([gun.to_dict() for gun in guns])

# API: search theo tên hoặc giá
@gun_bp.route('/search', methods=['GET'])
def search_by_name_or_price():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing search query'}), 400

    guns = gun_service.search_by_name_or_price(query)
    return jsonify([gun.to_dict() for gun in guns])

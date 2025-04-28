from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from inventory.inventory_service import get_inventory

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/api/inventory', methods=['GET'])
@jwt_required()
def api_get_inventory():
    """
    API lấy kho đồ của user
    """
    user_id = get_jwt_identity()
    items = get_inventory(user_id)

    return jsonify({
        "status": "success",
        "inventory": items
    }), 200

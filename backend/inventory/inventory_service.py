from database.nosql.mongoInterface import inventory_collection
from datetime import datetime

def add_item_to_inventory(user_id, skin_id, chest_id):
    """
    Thêm 1 skin mới vào kho đồ của user
    """
    inventory = inventory_collection.find_one({"_id": user_id})
    new_item = {
        "skin_id": skin_id,
        "chest_id": chest_id,
        "obtained_at": datetime.utcnow().isoformat(),
        "upgrade_level": 1
    }

    if not inventory:
        # Nếu chưa có inventory, tạo mới
        inventory = {
            "_id": user_id,
            "items": [new_item]
        }
        inventory_collection.insert_one(inventory)
    else:
        # Nếu đã có, thêm vào danh sách items
        inventory_collection.update_one(
            {"_id": user_id},
            {"$push": {"items": new_item}}
        )

def get_inventory(user_id):
    """
    Lấy danh sách skin của user
    """
    inventory = inventory_collection.find_one({"_id": user_id})
    if inventory:
        return inventory.get('items', [])
    else:
        return []

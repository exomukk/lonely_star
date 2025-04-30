from database.nosql.mongoInterface import inventory_collection
from datetime import datetime

def add_item_to_inventory(user_id, skin_id, chest_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    new_item = {
        "skin_id": skin_id,
        "chest_id": chest_id,
        "obtained_at": datetime.utcnow().isoformat(),
        "upgrade_level": 1,
        "isExecuting": False
    }

    if not inventory:
        inventory = {
            "_id": user_id,
            "items": [new_item]
        }
        inventory_collection.insert_one(inventory)
    else:
        inventory_collection.update_one(
            {"_id": user_id},
            {"$push": {"items": new_item}}
        )

def get_inventory(user_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if inventory:
        return inventory.get('items', [])
    else:
        return []

def check_item_executing(user_id, skin_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if not inventory:
        return False
    for item in inventory.get('items', []):
        if item.get('skin_id') == skin_id:
            return item.get('isExecuting', False)
    return False

def change_item_executing(user_id, skin_id, new_state: bool):
    inventory_collection.update_one(
        {"_id": user_id, "items.skin_id": skin_id},
        {"$set": {"items.$.isExecuting": new_state}}
    )

from database.nosql.mongoInterface import inventory_collection
from datetime import datetime
from inventory.inventory import InventoryItem

def add_item_to_inventory(user_id, skin_id, chest_id):
    inventory = inventory_collection.find_one({"_id": user_id})

    item = InventoryItem(
        skin_id=skin_id,
        chest_id=chest_id,
        obtained_at=datetime.utcnow().isoformat()
    )

    if not inventory:
        inventory = {
            "_id": user_id,
            "items": [item.to_dict()]
        }
        inventory_collection.insert_one(inventory)
    else:
        inventory_collection.update_one(
            {"_id": user_id},
            {"$push": {"items": item.to_dict()}}
        )

def get_inventory(user_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if inventory:
        return [InventoryItem.from_dict(i).to_dict() for i in inventory.get('items', [])]
    else:
        return []

def check_item_executing(user_id, skin_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if not inventory:
        return False
    for item in inventory.get('items', []):
        inv_item = InventoryItem.from_dict(item)
        if inv_item.skin_id == skin_id:
            return inv_item.isExecuting
    return False

def change_item_executing(user_id, skin_id, new_state: bool):
    inventory_collection.update_one(
        {"_id": user_id, "items.skin_id": skin_id},
        {"$set": {"items.$.isExecuting": new_state}}
    )

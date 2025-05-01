from database.nosql.mongoInterface import inventory_collection
from datetime import datetime
from inventory.inventory import InventoryItem

def add_item_to_inventory(user_id, skin_id, chest_id=None, source="chest"):
    inventory = inventory_collection.find_one({"_id": user_id})
    now = datetime.utcnow().isoformat()

    if not inventory:
        item = InventoryItem(skin_id, chest_id, now)
        inventory_collection.insert_one({
            "_id": user_id,
            "items": [item.to_dict()]
        })
    else:
        for item in inventory.get("items", []):
            if item["skin_id"] == skin_id:
                inventory_collection.update_one(
                    {"_id": user_id, "items.skin_id": skin_id},
                    {"$inc": {"items.$.quantity": 1}}
                )
                return
        item = InventoryItem(skin_id, chest_id, now)
        inventory_collection.update_one(
            {"_id": user_id},
            {"$push": {"items": item.to_dict()}}
        )

def remove_item_from_inventory(user_id, skin_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if not inventory:
        return False
    for item in inventory.get("items", []):
        if item["skin_id"] == skin_id:
            if item.get("quantity", 1) > 1:
                inventory_collection.update_one(
                    {"_id": user_id, "items.skin_id": skin_id},
                    {"$inc": {"items.$.quantity": -1}}
                )
            else:
                inventory_collection.update_one(
                    {"_id": user_id},
                    {"$pull": {"items": {"skin_id": skin_id}}}
                )
            return True
    return False

def get_inventory(user_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if inventory:
        return [InventoryItem.from_dict(i).to_dict() for i in inventory.get('items', [])]
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

def check_if_exist_in_inventory(user_id, skin_id):
    inventory = inventory_collection.find_one({"_id": user_id})
    if not inventory:
        return False
    return any(item["skin_id"] == skin_id for item in inventory.get("items", []))
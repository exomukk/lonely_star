from database.nosql.mongoInterface import chest_collection
from chest.chest import Chest
import random

def get_all_chests():
    chests = list(chest_collection.find({}))
    return [Chest.from_dict(chest) for chest in chests]

def get_chest_by_id(chest_id):
    chest_data = chest_collection.find_one({"_id": chest_id})
    if chest_data:
        return Chest.from_dict(chest_data)
    return None

def random_rarity(chest: Chest):
    distribution = chest.rarity_distribution
    pool = []
    for rarity, weight in distribution.items():
        pool += [rarity] * weight

    selected_rarity = random.choice(pool)
    return selected_rarity

def add_chest(chest: Chest):
    chest_collection.insert_one(chest.to_dict())

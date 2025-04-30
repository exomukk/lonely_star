from database.nosql.mongoInterface import chest_collection
import random

def get_all_chests():
    chests = list(chest_collection.find({}))
    return chests

def get_chest_by_id(chest_id):
    chest = chest_collection.find_one({"_id": chest_id})
    return chest

def random_rarity(chest_info):
    distribution = chest_info['rarity_distribution']

    pool = []
    for rarity, weight in distribution.items():
        pool += [rarity] * weight

    selected_rarity = random.choice(pool)
    return selected_rarity

def add_chest(chest_data):
    chest_collection.insert_one(chest_data)

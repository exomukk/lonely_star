from database.nosql.mongoInterface import chest_collection
from chest.chest import Chest
from random_heuristic.randomInterface import randomInterface
from user.userService import userService

def get_all_chests():
    chests = list(chest_collection.find({}))
    return [Chest.from_dict(chest) for chest in chests]

def get_chest_by_id(chest_id):
    chest_data = chest_collection.find_one({"_id": chest_id})
    if chest_data:
        return Chest.from_dict(chest_data)
    return None

def random_rarity(chest: Chest, user_id: str):
    distribution = chest.rarity_distribution
    total_weight = sum(distribution.values())

    lucky_seed = userService().getLuckySeedByID(user_id)
    if not lucky_seed:
        lucky_seed = randomInterface().pseudo_random()

    rand_index = randomInterface().randomize_100(user_id, lucky_seed) % total_weight

    cumulative = 0
    for rarity, weight in distribution.items():
        cumulative += weight
        if rand_index < cumulative:
            return rarity

    return list(distribution.keys())[-1]

def add_chest(chest: Chest):
    chest_collection.insert_one(chest.to_dict())

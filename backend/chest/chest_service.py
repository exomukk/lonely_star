from database.nosql.mongoInterface import chest_collection
import random

def get_all_chests():
    """
    Lấy toàn bộ danh sách các hòm.
    """
    chests = list(chest_collection.find({}))
    return chests

def get_chest_by_id(chest_id):
    """
    Lấy thông tin 1 hòm theo id.
    """
    chest = chest_collection.find_one({"_id": chest_id})
    return chest

def random_rarity(chest_info):
    """
    Dựa vào rarity_distribution của hòm, random ra rarity (common/rare/epic).
    """
    distribution = chest_info['rarity_distribution']

    # Biến tỉ lệ thành 1 list
    pool = []
    for rarity, weight in distribution.items():
        pool += [rarity] * weight

    # Random ra 1 rarity
    selected_rarity = random.choice(pool)
    return selected_rarity

def add_chest(chest_data):
    """
    Thêm 1 hòm mới vào collection (cho admin dùng).
    """
    chest_collection.insert_one(chest_data)

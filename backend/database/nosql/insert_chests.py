from database.nosql.mongoInterface import chest_collection

chests = [
    {
        "_id": "1",
        "name": "Common Chest",
        "price": -5,
        "rarity_distribution": {
            "common": 70,
            "rare": 25,
            "epic": 5
        }
    },
    {
        "_id": "2",
        "name": "Rare Chest",
        "price": -10,
        "rarity_distribution": {
            "common": 40,
            "rare": 40,
            "epic": 15,
            "legendary": 5
        }
    },
    {
        "_id": "3",
        "name": "Epic Chest",
        "price": -20,
        "rarity_distribution": {
            "common": 10,
            "rare": 30,
            "epic": 40,
            "legendary": 19,
            "mythic": 1
        }
    },
    {
        "_id": "4",
        "name": "Legendary Chest",
        "price": -50,
        "rarity_distribution": {
            "common": 5,
            "rare": 20,
            "epic": 25,
            "legendary": 40,
            "mythic": 10
        }
    },
    {
        "_id": "5",
        "name": "Mythic Chest",
        "price": -100,
        "rarity_distribution": {
            "rare": 40,
            "epic": 30,
            "legendary": 20,
            "mythic": 10
        }
    },
    {
        "_id": "0",
        "name": "Free Cash Chest",
        "price": 0,
        "reward_values": [0, 0, 0, 0, 10]
    }
]

# Xoá toàn bộ dữ liệu cũ trước khi insert mới
chest_collection.delete_many({})

# Insert nhiều hòm một lần
chest_collection.insert_many(chests)


print("Inserted chests successfully!")

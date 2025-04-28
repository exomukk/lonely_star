from database.nosql.mongoInterface import chest_collection

chests = [
    {
        "_id": "chest_common",
        "name": "Common Chest",
        "price": 5,
        "rarity_distribution": {
            "common": 70,
            "rare": 25,
            "epic": 5
        }
    },
    {
        "_id": "chest_rare",
        "name": "Rare Chest",
        "price": 10,
        "rarity_distribution": {
            "common": 40,
            "rare": 40,
            "epic": 15,
            "legendary": 5
        }
    },
    {
        "_id": "chest_epic",
        "name": "Epic Chest",
        "price": 20,
        "rarity_distribution": {
            "common": 10,
            "rare": 30,
            "epic": 40,
            "legendary": 19,
            "mythic": 1
        }
    },
    {
        "_id": "chest_legendary",
        "name": "Legendary Chest",
        "price": 50,
        "rarity_distribution": {
            "common": 5,
            "rare": 20,
            "epic": 25,
            "legendary": 40,
            "mythic": 10
        }
    },
    {
        "_id": "chest_mythic",
        "name": "Mythic Chest",
        "price": 100,
        "rarity_distribution": {
            "rare": 10,
            "epic": 20,
            "legendary": 30,
            "mythic": 40
        }
    }
]

# Insert nhiều hòm một lần
chest_collection.insert_many(chests)

print("Inserted chests successfully!")

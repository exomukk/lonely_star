from pymongo import MongoClient

mongo_client = MongoClient('mongodb://admin:admin123@localhost:27017')

mongo_db = mongo_client['game_db']

inventory_collection = mongo_db['inventories']
chest_collection = mongo_db['chests']

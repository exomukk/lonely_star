import json
import os

class Gun:
    def __init__(self, id, name, image, price, tierlist):
        self.id = id
        self.name = name
        self.image = image
        self.price = price
        self.tierlist = tierlist

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price,
            "tierlist": self.tierlist
        }

class GunService:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        with open(os.path.join(current_dir, 'weapons.json'), 'r', encoding='utf-8') as f:
            self.guns_data = json.load(f)
        self.guns = [Gun(**gun) for gun in self.guns_data]

    def get_by_price_range(self, min_price, max_price):
        return [gun for gun in self.guns if min_price <= gun.price <= max_price]

    def search_by_name_or_price(self, query):
        result = []
        for gun in self.guns:
            if gun.name.lower() == query.lower():
                result.append(gun)
            else:
                try:
                    if abs(gun.price - float(query)) < 0.01:  # Chênh lệch nhỏ để tránh lỗi float
                        result.append(gun)
                except:
                    continue
        return result

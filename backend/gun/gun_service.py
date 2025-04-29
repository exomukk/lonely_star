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

    def get_skin_by_rarity(self, rarity):
        """
        Lấy 1 skin random theo độ hiếm (rarity)
        """
        # Lọc tất cả skin thuộc tierlist tương ứng
        filtered_guns = [gun for gun in self.guns if gun.tierlist.lower() == rarity.lower()]

        if not filtered_guns:
            return None  # Nếu không có skin nào phù hợp

        import random
        selected_gun = random.choice(filtered_guns)
        return selected_gun.to_dict()

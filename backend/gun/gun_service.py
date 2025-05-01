import json
import random
from importlib import resources
from backend.gun.gun import Gun

class GunService:
    def __init__(self):
        with resources.files("backend.gun").joinpath("weapons.json").open("r", encoding="utf-8") as f:
            self.guns_data = json.load(f)
        self.guns = [Gun(**gun) for gun in self.guns_data]

    def get_by_price_range(self, min_price, max_price):
        return [gun for gun in self.guns if min_price <= gun.price <= max_price]

    def search_by_name_or_price(self, query):
        result = []
        query_lower = query.lower()
        for gun in self.guns:
            if query_lower in gun.name.lower():
                result.append(gun)
            else:
                try:
                    if abs(gun.price - float(query)) < 0.01:
                        result.append(gun)
                except:
                    continue
        return result

    def get_skin_by_rarity(self, rarity):
        filtered_guns = [gun for gun in self.guns if gun.tierlist.lower() == rarity.lower()]
        if not filtered_guns:
            return None
        selected_gun = random.choice(filtered_guns)
        return selected_gun.to_dict()

    def get_skin_by_id(self, skin_id):
        for gun in self.guns:
            if gun.id == skin_id:
                return gun.to_dict()
        return None

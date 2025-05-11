import json
import random
from importlib import resources
from gun.gun import Gun

class GunService:
    def __init__(self):
        with resources.files("gun").joinpath("weapons.json").open("r", encoding="utf-8") as f:
            self.guns_data = json.load(f)
            self.guns_data = list(self.guns_data.values())
        self.guns = [Gun(**gun) for gun in self.guns_data]

    def get_by_price_range(self, min_price, max_price):
        return [gun for gun in self.guns if min_price <= gun.price <= max_price]

    def search_by_name(self, query):
        query_lower = str(query).lower()
        result = []
        for gun in self.guns:
            if query_lower in gun.name.lower():
                result.append(gun)

        return result

    def get_skin_by_rarity(self, rarity):
        filtered_guns = [gun for gun in self.guns if gun.tierlist.lower() == rarity.lower()]
        if not filtered_guns:
            return None
        selected_gun = random.choice(filtered_guns)
        return selected_gun.to_dict()

    def get_skins_by_rarity(self, rarity):
        return [
            gun.to_dict()
            for gun in self.guns
            if hasattr(gun, 'tierlist') and gun.tierlist.lower() == rarity.lower()
        ]

    def get_skin_by_id(self, skin_id):
        for gun in self.guns:
            if gun.id == skin_id:
                data = gun.to_dict()
                print("gun data", data)
                return data
        return None

    def get_skin_by_id_object(self,skin_id):
        print("called")
        for gun in self.guns:
            # print(gun.id, "+", skin_id)
            if str(gun.id) == str(skin_id):
                print(gun.id)
                return gun
        return None
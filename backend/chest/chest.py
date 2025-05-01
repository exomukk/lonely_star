class Chest:
    def __init__(self, _id, name, price, rarity_distribution):
        self.id = _id
        self.name = name
        self.price = price
        self.rarity_distribution = rarity_distribution

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "price": self.price,
            "rarity_distribution": self.rarity_distribution
        }

    @staticmethod
    def from_dict(data):
        return Chest(
            _id=data.get("_id"),
            name=data.get("name"),
            price=data.get("price"),
            rarity_distribution=data.get("rarity_distribution", {})
        )

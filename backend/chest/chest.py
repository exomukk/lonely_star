class Chest:
    def __init__(self, _id, name, price, rarity_distribution, reward_type=None, reward_values=None):
        self.id = _id
        self.name = name
        self.price = price
        self.rarity_distribution = rarity_distribution
        self.reward_type = reward_type
        self.reward_values = reward_values or []

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
            rarity_distribution=data.get("rarity_distribution", {}),
            reward_type = data.get('reward_type'),
            reward_values = data.get('reward_values', [])
        )

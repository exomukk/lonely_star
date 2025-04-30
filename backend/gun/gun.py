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

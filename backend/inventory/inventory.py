class InventoryItem:
    def __init__(self, skin_id, chest_id, obtained_at, isExecuting=False, quantity=1):
        self.skin_id = skin_id
        self.chest_id = chest_id
        self.obtained_at = obtained_at
        self.isExecuting = isExecuting
        self.quantity = quantity

    def to_dict(self):
        return {
            "skin_id": self.skin_id,
            "chest_id": self.chest_id,
            "obtained_at": self.obtained_at,
            "isExecuting": self.isExecuting,
            "quantity": self.quantity
        }

    @staticmethod
    def from_dict(data):
        return InventoryItem(
            skin_id=data["skin_id"],
            chest_id=data.get("chest_id", None),
            obtained_at=data["obtained_at"],
            isExecuting=data.get("isExecuting", False),
            quantity=data.get("quantity", 1)
        )

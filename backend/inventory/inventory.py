class InventoryItem:
    def __init__(self, skin_id, chest_id, obtained_at, upgrade_level=1, isExecuting=False):
        self.skin_id = skin_id
        self.chest_id = chest_id
        self.obtained_at = obtained_at
        self.upgrade_level = upgrade_level
        self.isExecuting = isExecuting

    def to_dict(self):
        return {
            "skin_id": self.skin_id,
            "chest_id": self.chest_id,
            "obtained_at": self.obtained_at,
            "upgrade_level": self.upgrade_level,
            "isExecuting": self.isExecuting
        }

    @staticmethod
    def from_dict(data):
        return InventoryItem(
            skin_id=data["skin_id"],
            chest_id=data["chest_id"],
            obtained_at=data["obtained_at"],
            upgrade_level=data.get("upgrade_level", 1),
            isExecuting=data.get("isExecuting", False)
        )

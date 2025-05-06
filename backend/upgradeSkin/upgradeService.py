import random_heuristic.randomInterface as randomInterface
import upgradeSkin.upgradeRecord as upgradeRoom
import time
from random_heuristic.randomInterface import randomInterface
from gun.gun_service import GunService
from user.userService import userService
import inventory.inventory_service as InventoryService
from database.sql.dbInterface import DatabaseInterface as dbInterface

class upgradeRoomService:
    def __init__(self):
        pass

    def rollRate(self,userID, userWeaponID, expectedWeaponID):
        rate = 0
        if InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            userWeaponPrice = GunService.get_skin_by_id_object(userWeaponID).price
            expectedWeaponPrice = GunService.get_skin_by_id(expectedWeaponID).price
            if expectedWeaponPrice is None or userWeaponPrice is None:
                return 0
            rate = userWeaponPrice / expectedWeaponPrice * 100
        return rate

    def userUpgradeRecord(self,userID):
        try:
            return dbInterface.getUpgradeRecord(userID)
        # Sample response:
        # [
        #     (1, 'user123', 'weapon5', 'weapon8', 75.5, 1689245780, 1),
        #     (2, 'user123', 'weapon8', 'weapon12', 50.0, 1689247890, 0),
        #     (3, 'user123', 'weapon6', 'weapon9', 60.5, 1689345678, 1)
        # ]
        except:
            return {"status": "error", "message": "No upgrade record found"}

    def newUpgradeRecord(self,userID, userWeaponID, expectedWeaponID, success):
        successRate = self.rollRate(userID, userWeaponID, expectedWeaponID)
        upgradeDate = time.time()
        dbInterface.addUpgradeRecord(userWeaponID, expectedWeaponID, successRate, upgradeDate, success)

    def upgradeSuccess(self,userID, userWeaponID, expectedWeaponID):
        try:
            InventoryService.remove_item_from_inventory(userID, userWeaponID)
            InventoryService.add_item_to_inventory(userID, expectedWeaponID, None, "upgrade")
            self.newUpgradeRecord(userID, userWeaponID, expectedWeaponID, True)
            return True
        except:
            print("Failed to save new skin ID to user, reverting")
            return False

    def upgradeFailed(self,userID, userWeaponID, expectedWeaponID):
        try:
            InventoryService.remove_item_from_inventory(userID, userWeaponID)
            self.newUpgradeRecord(userID, userWeaponID, expectedWeaponID, False)
            return True
        except:
            print("Failed to remove old skin ID to user, reverting")
            return False

    def executeRoll(self,userID, userWeaponID, expectedWeaponID, startRange, endRange):
        if InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            if InventoryService.check_item_executing(userWeaponID, "false"):
                if abs(endRange - startRange) % 360 - self.rollRate(userID, userWeaponID, expectedWeaponID) < 2:
                    InventoryService.change_item_executing(userWeaponID,
                                                           "true")  # nhac beo them cai FOR UPDATE o database
                    if userService.getLuckySeedByID(userID) is None:
                        luckySeed = randomInterface.pseudo_random()
                    else:
                        luckySeed = userService.getLuckySeedByID(userID)
                    result = randomInterface.randomize_360(randomInterface.pseudo_random(), userID, luckySeed)
                    if startRange <= result <= endRange:
                        self.upgradeSuccess(userID, userWeaponID, expectedWeaponID)
                        return True
                    else:
                        self.upgradeFailed(userID, userWeaponID, expectedWeaponID)
                        return False
                print("Roll rate range error")
                return False
            print("Item is executing")
            return False
        print("Item not found in inventory")
        return False


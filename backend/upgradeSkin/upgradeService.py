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
        self.userService = userService()
        self.GunService = GunService()
        self.InventoryService = InventoryService
        self.randomInterface = randomInterface()
        pass

    def rollRate(self,userID, userWeaponID, expectedWeaponID):
        rate = 0
        if self.InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            userWeaponPrice = self.GunService.get_skin_by_id_object(userWeaponID).price
            expectedWeaponPrice = self.GunService.get_skin_by_id_object(expectedWeaponID).price
            print(userWeaponPrice)
            if expectedWeaponPrice is None or userWeaponPrice is None:
                return 0
            rate = userWeaponPrice / expectedWeaponPrice * 100

        else:
            print('no exist skin')
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
        print("Upgrade success")
        try:
            InventoryService.remove_item_from_inventory(userID, userWeaponID)
            InventoryService.add_item_to_inventory(userID, expectedWeaponID, None, "upgrade")
            self.newUpgradeRecord(userID, userWeaponID, expectedWeaponID, True)
            return True
        except:
            print("Failed to save new skin ID to user, reverting")
            return False

    def upgradeFailed(self,userID, userWeaponID, expectedWeaponID):
        print("Upgrade failed")
        try:
            InventoryService.remove_item_from_inventory(userID, userWeaponID)
            self.newUpgradeRecord(userID, userWeaponID, expectedWeaponID, False)
            return True
        except:
            print("Failed to remove old skin ID to user, reverting")
            return False

    def executeRoll(self,userID, userWeaponID, expectedWeaponID, startRange, endRange):
        if InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            #if InventoryService.check_item_executing(userWeaponID, False):
                #if abs(endRange - startRange) % 360 - self.rollRate(userID, userWeaponID, expectedWeaponID) < 2:

                    self.InventoryService.change_item_executing(userID,userWeaponID,True)

                    result = self.randomInterface.randomize_360(self.randomInterface.pseudo_random(), userID, self.randomInterface.pseudo_random())

                    if startRange <= result <= endRange:
                        self.upgradeSuccess(userID, userWeaponID, expectedWeaponID)
                        print("success-upgrade")
                        return True
                    else:
                        self.upgradeFailed(userID, userWeaponID, expectedWeaponID)
                        print("fail-upgrade")
                        return False

                #print("Roll rate range error")
                #return False
            #print("Item is executing")
            #return False
        print("Item not found in inventory")
        return False


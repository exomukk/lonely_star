import random_heuristic.randomInterface as randomInterface
import upgradeSkin.upgradeRecord as upgradeRoom
import time
from random_heuristic.randomInterface import randomInterface
from gun.gun_service import GunService
from user.userService import userService
import inventory.inventory_service as InventoryService
from database.sql.dbInterface import DatabaseInterface
class upgradeRoomService:
    def __init__(self):
        pass

    def rollRate(self,userID,userWeaponID,expectedWeaponID):
        rate = 0
        if InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            userWeaponPrice = GunService.get_skin_by_id_object(userWeaponID).price
            expectedWeaponPrice = GunService.get_skin_by_id(expectedWeaponID).price
            if expectedWeaponPrice is None or userWeaponPrice is None:
                return 0
            rate = userWeaponPrice/expectedWeaponPrice * 100
        return rate

    def executeRoll(self,userID,userWeaponID,expectedWeaponID,startRange,endRange):
        if InventoryService.check_if_exist_in_inventory(userID, userWeaponID):
            if InventoryService.check_item_executing(userWeaponID, "false"):
                if abs(endRange - startRange)%360-self.rollRate(userID, userWeaponID, expectedWeaponID)<2:
                    InventoryService.change_item_executing(userWeaponID,"true") #nhac beo them cai FOR UPDATE o database
                    if userService.getLuckySeedByID(userID) is None:
                        luckySeed=randomInterface.randomize(randomInterface.pseudo_random())
                    else:
                        luckySeed=userService.getLuckySeedByID(userID)
                    result = randomInterface.randomize(randomInterface.pseudo_random(), userID, luckySeed)
                    if startRange <= result <= endRange:
                        self.upgradeSuccess(userID,userWeaponID,expectedWeaponID)
                        return { "success": True, "reason": "You lucky today lil bro 🎁" }
                    else:
                        self.upgradeFailed(userID,userWeaponID,expectedWeaponID)
                        return { "success": False, "reason": "How about trying higher rate 🔥" }
                return { "success": False, "reason": "Try to make it 100% success huh 🤓" }
            return { "success": False, "reason": "Haha, try to upgrade the skin 2 times ? Not applicable here 😉" }
        return { "success": False, "reason": "You don't have the skin, don't try to spam with custom responses 😊" }

    def upgradeSuccess(self,userID,userWeaponID,expectedWeaponID):
        try:
            InventoryService.remove_item_from_inventory(userID, userWeaponID)
            InventoryService.addItem(userID, expectedWeaponID)
            self.newUpgradeRecord(userID,userWeaponID,expectedWeaponID,True)
        except:
            print("Failed to save new skin ID to user, reverting")
    def upgradeFailed(self,userID,userWeaponID,expectedWeaponID):
        try:
            InventoryService.remove_item_from_inventory(userID,userWeaponID)
            self.newUpgradeRecord(userID,userWeaponID,expectedWeaponID,False)
        except:
            print("Failed to remove old skin ID to user, reverting")

    def newUpgradeRecord(self,userID,userWeaponID,expectedWeaponID,success):
        successRate=self.rollRate(userID,userWeaponID,expectedWeaponID)
        upgradeDate = time.time()
        DatabaseInterface.addUpgradeRecord(userID,userWeaponID,expectedWeaponID,successRate,upgradeDate,success)

    def userUpgradeRecord(self,userID):
        try:
            return DatabaseInterface.getUpgradeRecord(userID)
        # Sample response:
        # [
        #     (1, 'user123', 'weapon5', 'weapon8', 75.5, 1689245780, 1),
        #     (2, 'user123', 'weapon8', 'weapon12', 50.0, 1689247890, 0),
        #     (3, 'user123', 'weapon6', 'weapon9', 60.5, 1689345678, 1)
        # ]
        except:
            return { "status": "error", "message": "No upgrade record found" }
#nhac beo them rollback cho addItem va removeItem
#nhac beo them FOR UPDATE cho addStateToItem
import random_heuristic.randomInterface as randomInterface
import upgradeSkin.upgradeRecord as upgradeRoom
import time
from random_heuristic.randomInterface import randomInterface
from gun.gun_service import GunService
from user.userService import userService
from inventory.inventory_service import InventoryService
from database.sql.dbInterface import DatabaseInterface
class upgradeRoomService:
    def __init__(self):
        pass

    def rollRate(self,userID,userWeaponID,expectedWeaponID):
        if (InventoryService.checkIfExistInInventory(userID,userWeaponID)):
            userWeaponPrice = GunService.getPrice(userWeaponID)
            expectedWeaponPrice = GunService.getPrice(expectedWeaponID)
            rate = userWeaponPrice/expectedWeaponPrice * 100
        return rate

    def executeRoll(self,userID,userWeaponID,expectedWeaponID,startRange,endRange):
        if (InventoryService.checkIfExistInInventory(userID, userWeaponID)):
            if (InventoryService.checkWeaponState(userWeaponID,"false")):
                if(abs(endRange-startRange)%360-self.rollRate(userID,userWeaponID,expectedWeaponID)<2):
                    InventoryService.addStateToItem(userWeaponID,"true") #nhac beo them cai FOR UPDATE o database
                    if (userService.getLuckySeedByID(userID)== None):
                        luckySeed=randomInterface.randomize(randomInterface.pseudo_random())
                    else:
                        luckySeed=userService.getLuckySeedByID(userID)
                    result = randomInterface.randomize(randomInterface.pseudo_random(), userID, luckySeed)
                    if (result >= startRange and result <= endRange):
                        self.upgradeSuccess(userID,userWeaponID,expectedWeaponID)
                        return { "success": True, "reason": "You lucky today lil bro 🎁" }
                    else:
                        self.upgradeFailed(userID,userWeaponID,expectedWeaponID)
                        return { "success": False, "reason": "How about trying higher rate 🔥" }
                return { "success": False, "reason": "Try to make it 100% success huh 🤓" }
            return { "success": False, "reason": "Haha, try to upgrade the skin 2 times ? Not applicable here 😉" }
        return { "success": False, "reason": "You don't have the skin, don't try to fake with custom responses" }

    def upgradeSuccess(self,userID,userWeaponID,expectedWeaponID):
        try:
            InventoryService.removeItem(userID, userWeaponID)
            InventoryService.addItem(userID, expectedWeaponID)
            self.newUpgradeRecord(userID,userWeaponID,expectedWeaponID,True)
        except:
            print("Failed to save new skin ID to user, reverting")
    def upgradeFailed(self,userID,userWeaponID,expectedWeaponID):
        try:
            InventoryService.removeItem(userID,userWeaponID)
            self.newUpgradeRecord(userID,userWeaponID,expectedWeaponID,False)
        except:
            print("Failed to remove old skin ID to user, reverting")

    def newUpgradeRecord(self,userID,userWeaponID,expectedWeaponID,success):
        successRate=self.rollRate(userID,userWeaponID,expectedWeaponID)
        upgradeDate = time.time()
        DatabaseInterface.addUpgradeRecord(userID,userWeaponID,expectedWeaponID,successRate,upgradeDate,success)

#nhac beo them rollback cho addItem va removeItem
#nhac beo them FOR UPDATE cho addStateToItem
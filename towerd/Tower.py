from enum import Enum

# We might need to move this enum to the game class
class TowerSubclass(Enum):
    Soldier = 1
    Archer = 2
    Mage = 3

class Tower:
    # Constructor
    def __init__(self, subclass, x, y):
        self.xCoord = x
        self.yCoord = y
        if(subclass == TowerSubclass.Soldier):
            self.subclass = TowerSubclass.Soldier
            self.damage = 10
            self.range = 2
            self.level = 0
        if(subclass == TowerSubclass.Archer):
            self.subclass = TowerSubclass.Archer
            self.damage = 7
            self.range = 5
            self.level = 0
        if(subclass == TowerSubclass.Mage):
            self.subclass = TowerSubclass.Mage
            self.damage = 10
            self.range = 4
            self.level = 0

    # Getters
    def getSubclass(self):
        return self.subclass

    def getDamage(self):
        return self.damage

    def getRange(self):
        return self.range

    def getLevel(self):
        return self.level

    # Upgrade
    def upgrade(self):
        if(self.level <= 2):
            self.level+= 1
            self.damage+=3

    # Get cost for upgrading, these numbers can be changed later depending on how much money the player gets per enemy/wave
    def getUpgradeCost(self):
        if(self.subclass == TowerSubclass.Soldier):
            if(self.level == 0):
                return 100
            elif(self.level == 1):
                return 150
            else:
                return 200
        elif(self.subclass == TowerSubclass.Archer):
            if (self.level == 0):
                return 150
            elif (self.level == 1):
                return 200
            else:
                return 250
        else:
            if (self.level == 0):
                return 200
            elif (self.level == 1):
                return 250
            else:
                return 300
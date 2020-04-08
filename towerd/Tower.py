from enum import Enum
class TowerSubclass(Enum):
    Soldier = 1
    Archer = 2
    Mage = 3
class Tower:
    # Constructor
    def __init__(self, subclass):
        if(subclass == Soldier):
            self.subclass = Soldier
            self.health = 100
            self.damage = 10
            self.range = 2
            self.level = 0
        if(subclass == Archer):
            self.subclass = Archer
            self.health = 75
            self.damage = 7
            self.range = 5
            self.level = 0
        if(subclass == Mage):
            self.subclass = Mage
            self.health = 125
            self.damage = 10
            self.range = 4
            self.level = 0

    # Getters
    def getSubclass(self):
        return self.subclass

    def getHealth(self):
        return self.health

    def getDamage(self):
        return self.damage

    def getRange(self):
        return self.range

    def getLevel(self):
        return self.level
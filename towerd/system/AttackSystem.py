import math, kdtree

from ..System import System


class AttackSystem(System):
    def update(self, dt, state):
        for entity in self.entities:
            # Find entity nearest to this entity
            tree = kdtree.create([entity.x, entity.y])
            nearestEntity = tree.search_nn(entity.x, entity.y)

            # if nearestEntity is attackable
            if(nearestEntity.attackable == True):
                # calculate distance between entity and nearestEntity
                distance = math.sqrt(math.pow(nearestEntity.x - entity.x, 2) + math.pow(nearestEntity.y - entity.y, 2))

                # if nearestEntity is within range
                if(distance <= entity.attackRange):
                    # Do the damage to nearest entity

                    # if it has a shield, subtract from shield
                    if(nearestEntity.shield > 0):
                        nearestEntity.shield -= entity.dmg

                        # If the shield is below 0, deal excess damage to health
                        if(nearestEntity.shield <= 0):
                            excessDamage = 0 - nearestEntity.shield
                            nearestEntity.health -= excessDamage
                            
                    else:
                        # nearestEntity has no shield, deal damage directly to health
                        nearestEntity.health -= entity.dmg

                    # If nearestEntity is dead kill it
                    if(nearestEntity.health <= 0):
                        # it is dead
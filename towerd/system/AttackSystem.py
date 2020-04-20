import math, kdtree

from ..System import System


class AttackSystem(System):
    def update(self, dt, state, attackComps, vitalComps, locComps):
        for entity in self.entities:
            entityLocComp = locComps[entity.ID]
            entityAttackComp = attackComps[entity.ID]

            # Find entity nearest to this entity
            tree = self.state['tree']
            nearestEntity = tree.search_nn(entityLocComp.x, entityLocComp.y)
            nearestEntityAttackComp = attackComps[nearestEntity.ID]
            nearestEntityLocComp = locComps[nearestEntity.ID]
            nearestEntityVitalComp = vitalComps[nearestEntity.ID]

            # if nearestEntity is attackable
            if(nearestEntityAttackComp.attackable == True):
                # calculate distance between entity and nearestEntity
                distance = math.sqrt(math.pow(nearestEntityLocComp.x - entityLocComp.x, 2) + math.pow(nearestEntityLocComp.y - entityLocComp.y, 2))

                # if nearestEntity is within range
                if(distance <= entityLocComp.attackRange):
                    # Do the damage to nearest entity

                    # if it has a shield, subtract from shield
                    if(nearestEntityVitalComp.shield > 0):
                        nearestEntityVitalComp.shield -= entityAttackComp.dmg

                        # If the shield is below 0, deal excess damage to health
                        if(nearestEntityVitalComp.shield <= 0):
                            excessDamage = 0 - nearestEntityVitalComp.shield
                            nearestEntityVitalComp.health -= excessDamage

                    else:
                        # nearestEntity has no shield, deal damage directly to health
                        nearestEntityVitalComp.health -= entityAttackComp.dmg

                    # If nearestEntity is dead kill it
                    if(nearestEntityVitalComp.health <= 0):
                        # it is dead
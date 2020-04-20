import math
import kdtree

from ..System import System


class AttackSystem(System):
    def update(self, dt, state, attackComps, vitalComps, locComps):
        for entity in self.entities:
            tree = self.state['tree']
            entityLocComp = locComps[entity.ID]
            entityAttackComp = attackComps[entity.ID]

            # If the attacker doesn't already have a target, set the target to be the nearest entity
            if(entityAttackComp.target == None):
                # Find entity nearest to this entity
                nearestEntity = tree.search_nn(entityLocComp.x, entityLocComp.y)
                entityAttackComp.target = nearestEntity

            targetAttackComp = attackComps[entityAttackComp.target.ID]
            targetLocComp = locComps[entityAttackComp.target.ID]
            targetVitalComp = vitalComps[entityAttackComp.target.ID]

            # if target is attackable
            if(targetAttackComp.attackable == True):
                # calculate distance between entity and target
                distance = math.sqrt(math.pow(targetLocComp.x - entityLocComp.x, 2) + math.pow(targetLocComp.y - entityLocComp.y, 2))

                # Calculate total damage based on entity's damage and the amount of time passed vs. attack speed
                totalDamage = entityAttackComp.attackSpeed * dt * entityAttackComp.dmg

                # if target is within range
                if(distance <= entityLocComp.attackRange):
                    # Do the damage to nearest entity

                    # if it has a shield, subtract from shield
                    if(targetVitalComp.shield > 0):
                        targetVitalComp.shield -= totalDamage

                        # If the shield is below 0, deal excess damage to health
                        if(targetVitalComp.shield <= 0):
                            excessDamage = 0 - targetVitalComp.shield
                            targetVitalComp.health -= excessDamage

                    else:
                        # target has no shield, deal damage directly to health
                        targetVitalComp.health -= totalDamage

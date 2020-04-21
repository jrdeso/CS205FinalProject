import math

from ..System import System


class AttackSystem(System):
    def update(self, dt, state, attackComps, vitalComps, locComps, factionComps):
        for entity in self.entities:
            tree = state["tree"]
            entityLocComp = locComps[entity.ID]
            entityAttackComp = attackComps[entity.ID]
            entityFactionComp = factionComps[entity.ID]

            def calcDist(x0, y0, x1, y1):
                return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

            # If the attacker doesn't already have a target, set the target to
            # be the nearest, in-range entity of the opposite faction
            if not entityAttackComp.target:
                ep2ds = tree.search_nn_dist(
                    (entityLocComp.x, entityLocComp.y), entityAttackComp.attackRange
                )
                ep2ds = sorted(
                    ep2ds, key=lambda t: calcDist(entityLocComp.x, entityLocComp.y, *t)
                )

                for ep2d in ep2ds:
                    target = ep2d.entity
                    targetFactionComp = factionComps[target.ID]
                    targetAttackComp = attackComps[target.ID]

                    if (
                        targetFactionComp != entityFactionComp
                        and targetAttackComp.attackable
                    ):
                        entityAttackComp.target = target
                continue

            # unset targets that are too far
            targetLocComp = locComps[entityAttackComp.target.ID]
            distance = calcDist(
                entityLocComp.x, entityLocComp.y, targetLocComp.x, targetLocComp.y
            )
            if distance > entityAttackComp.attackRange:
                entityAttackComp.target = None
                continue

            targetVitalComp = vitalComps[entityAttackComp.target.ID]
            totalDamage = entityAttackComp.attackSpeed * dt * entityAttackComp.dmg

            # Do the damage to nearest entity
            if targetVitalComp.shield > 0:
                targetVitalComp.shield -= totalDamage

                if targetVitalComp.shield <= 0:
                    excessDamage = 0 - targetVitalComp.shield
                    targetVitalComp.health -= excessDamage
            else:
                targetVitalComp.health -= totalDamage

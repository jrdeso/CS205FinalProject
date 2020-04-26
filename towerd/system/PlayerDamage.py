from towerd.System import System
from towerd.Map import PathType
from towerd.component.Attack import Attack
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital


class PlayerDamage(System):
    def update(self, dt, state, ecsManager):
        factionComps = ecsManager.getComponentArr(Faction)
        locComps = ecsManager.getComponentArr(LocationCartesian)
        attackComps = ecsManager.getComponentArr(Attack)
        vitalComps = ecsManager.getComponentArr(Vital)

        # Get vital components of player
        playerVitalComp = vitalComps[state.player.ID]

        # Get all PATH_END nodes
        pathEndNodes = []
        for nodeID, mapNode in state.map.nodes.items():
            if mapNode.pathType == PathType.PATH_END:
                pathEndNodes.append(mapNode)

        # Iterate through all entites
        for entity in self.entities:
            # Get components of the entity
            entityFactionComp = factionComps[entity.ID]
            entityLocComp = locComps[entity.ID]
            entityAttackComp = attackComps[entity.ID]
            entityVitalComp = vitalComps[entity.ID]

            # If the entity is a mob
            if entityFactionComp.faction == 0:
                # If the mob is at any PATH_END node
                for endNode in pathEndNodes:
                    if entityLocComp.x == endNode.x and entityLocComp.y == endNode.y:
                        # Calculate total damage based on mob's attack and attack speed
                        totalDamage = entityAttackComp.attackSpeed * entityAttackComp.dmg

                        # If player has a shield deal damage to shield
                        if playerVitalComp.shield > 0:
                            playerVitalComp.shield -= totalDamage

                            # If the player's shield is depeleted deal excess damage to the player
                            if playerVitalComp.shield <= 0:
                                excessDamage = 0 - playerVitalComp.shield
                                playerVitalComp.health -= excessDamage

                        # If player has no shield deal damage to health
                        else:
                            playerVitalComp.health -= totalDamage

                        # kill entity
                        entityVitalComp.health = 0
                        entityVitalComp.shield = 0
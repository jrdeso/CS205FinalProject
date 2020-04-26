import random

from towerd.Map import PathType
from towerd.System import System
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.MapNode import MapNode
from towerd.component.Movement import Movement


class SpawnSystem(System):
    def update(self, dt, state, ecsManager):
        mapNodes = ecsManager.getComponentArr(MapNode)
        locComps = ecsManager.getComponentArr(LocationCartesian)

        # Get all path_start MapNodes and add them to a list
        pathStartNodes = []
        for entity in self.entities:
            mapNode = mapNodes[entity.ID]
            if mapNode.pathType == PathType.PATH_START:
                pathStartNodes.append(entity)

        # Get the number of mobs based on what wave it is
        waveNum = state.wave
        numMobs = int(max(10, 10 * random.random() * waveNum))

        from towerd.Game import GameEntityType, Game
        for i in range(numMobs):
            pathStartEntity = random.choice(pathStartNodes)
            pathStartNode = mapNodes[pathStartEntity.ID]

            pathTargetEntity = random.choice(pathStartNode.edges)

            locComp = locComps[pathStartEntity.ID]
            pathStartX = locComp.x
            pathStartY = locComp.y

            mobType = random.choice([GameEntityType.ORC])
            mob = Game.createMob(ecsManager, state, mobType, pathStartX, pathStartY)
            if mob:
                movement_comp = ecsManager.getEntityComponent(mob, Movement)
                movement_comp.fromNode = pathStartEntity
                movement_comp.destNode = pathTargetEntity

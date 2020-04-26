import random

from towerd.System import System
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.MapNode import MapNode, PathType
from towerd.component.Movement import Movement


class SpawnSystem(System):
    def __init__(self):
        super().__init__()
        self.lastSpawned = 0
        self.spawnRemaining = 0
        self.baseRate = 5000
        self.spawnRate = self.baseRate

    def addWave(self, wave):
        # Get the number of mobs based on what wave it is
        waveNum = wave
        numMobs = int(max(10, 10 * random.random() * waveNum))
        self.spawnRemaining += numMobs

    def update(self, dt, state, ecsManager):
        self.lastSpawned += dt

        mapNodes = ecsManager.getComponentArr(MapNode)
        locComps = ecsManager.getComponentArr(LocationCartesian)

        self.spawnRate = min(self.baseRate, self.baseRate / (self.spawnRemaining + 1))

        # Get all path_start MapNodes and add them to a list
        pathStartNodes = []
        for entity in self.entities:
            mapNode = mapNodes[entity.ID]
            if mapNode.pathType == PathType.PATH_START:
                pathStartNodes.append(entity)

        from towerd.Game import GameEntityType, Game
        if self.lastSpawned > self.spawnRate and self.spawnRemaining > 0:
            self.lastSpawned = 0
            self.spawnRemaining -= 1

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

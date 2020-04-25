import random

from towerd.Game import GameEntityType, Game
from towerd.Map import PathType
from towerd.System import System
from towerd.component.Movement import Movement


class SpawnSystem(System):
    def update(self, dt, state, ecsManager):
        # Get all path_start MapNodes and add them to a list
        pathStartNodes = []
        for nodeID, mapNode in state.map.nodes.items():
            if mapNode.pathType == PathType.PATH_START:
                pathStartNodes.append(mapNode)

        # Get the number of mobs based on what wave it is
        waveNum = state.wave
        numMobs = 0
        if waveNum == 1:
            numMobs = 5
        elif waveNum == 2:
            numMobs = 10
        elif waveNum == 3:
            numMobs = 15
        elif waveNum == 4:
            numMobs = 20
        elif waveNum == 5:
            numMobs = 25

        for i in range(numMobs):
            pathStartNode = random.choice(pathStartNodes)
            pathTargetID = random.choice(state.map.map[pathStartNode.id])
            pathTargetNode = state.map.nodes[pathTargetID]

            pathStartX = pathStartNode.x
            pathStartY = pathStartNode.y

            mobType = random.choice([GameEntityType.ORC])
            mob = Game.createMob(ecsManager, state, mobType, pathStartX, pathStartY)
            if mob:
                ecsManager.addEntityComponent(
                    mob, Movement(0.3, pathStartNode.id, pathTargetNode.id)
                )

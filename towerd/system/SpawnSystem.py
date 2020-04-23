import random

from towerd.System import System
from towerd.component.Attack import Attack
from towerd.component.Movement import Movement
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital


class SpawnSystem(System):
    def update(self, dt, state, ecs_manager):
        # Get all path_start MapNodes and add them to a list
        pathStartCoords = []
        for mapNode in state.map.nodes:
            if mapNode.pathType == 'path_start':
                pathStartCoords.append(mapNode)

        # Get the number of mobs based on what wave it is
        waveNum = state.wave
        numMobs = 0
        if(waveNum == 1):
            numMobs = 5
        elif(waveNum == 2):
            numMobs = 10
        elif(waveNum == 3):
            numMobs = 15
        elif(waveNum == 4):
            numMobs = 20
        elif(waveNum == 5):
            numMobs = 25

        # create the  mobs
        for i in range(numMobs):
            mob = ecs_manager.createEntity()
            # Get x and y coords from a random path_start
            pathStartNode = random.choice(pathStartCoords)
            pathTargetNode = random.choice(state.map[pathStartNode])
            pathStartX = pathStartNode.x
            pathStartY = pathStartNode.y

            ecs_manager.addEntityComponent(mob, LocationCartesian(pathStartX, pathStartY))
            ecs_manager.addEntityComponent(mob, Vital(100, 10))
            ecs_manager.addEntityComponent(mob, Movement(0.3, pathStartNode.id, pathTargetNode.id))
            ecs_manager.addEntityComponent(mob, Attack(0.01, 2, 5, None, True))
            ecs_manager.addEntityComponent(mob, Faction(0))

            #state.entites.update({mob : 0})

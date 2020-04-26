import math
import random

from towerd.System import System
from towerd.component.Movement import Movement
from towerd.component.LocationCartesian import LocationCartesian
from towerd.Map import PathType


class MovementSystem(System):
    def update(self, dt, state, ecsManager):
        """
        Move entities with movement and location components.

        :param dt: change in time
        :param state: the game state
        :param ecsManager: ECS Manager
        """
        for entity in self.entities:
            movementComps = ecsManager.getComponentArr(Movement)
            locComps = ecsManager.getComponentArr(LocationCartesian)

            # grab movement related details from the current entity
            movementComp = movementComps[entity.ID]
            speed = movementComp.speed
            fromNode = movementComp.fromNode
            destNode = movementComp.destNode

            m = state.map

            # get the current location and target destination
            # TODO: Check that entity has a target destination
            fromNode = m.nodes[fromNode]
            destNode = m.nodes[destNode]
            locComp = locComps[entity.ID]

            fromX, fromY = locComp.x, locComp.y
            destX, destY = destNode.x, destNode.y

            # calculate the new coordinates
            totalDiffX = destX - fromX
            totalDiffY = destY - fromY

            theta = math.atan2(totalDiffY, totalDiffX)
            dl = speed * dt

            dx = dl * math.cos(theta)
            dy = dl * math.sin(theta)

            if fromX < destX and (newX := fromX + dx) < destX:
                locComp.x = newX
            elif fromX > destX and (newX := fromX - dx) > destX:
                locComp.x = newX
            else:
                locComp.x = destX

            if fromY < destY and (newY := fromY + dy) < destY:
                locComp.y = newY
            elif fromY > destY and (newY := fromY - dy) > destY:
                locComp.y = newY
            else:
                locComp.y = destY


            # Get possible destination nodes
            pathEndNodes = []
            for nodeID, mapNode in state.map.nodes.items():
                if mapNode.pathType == PathType.PATH_END:
                    pathEndNodes.append(mapNode)

            # If the entity is at the destination node, update to next destination node
            if(locComp.x == destNode.x and locComp.y == destNode.y):
                newDestNode = random.choice(pathEndNodes)
                locComp.destNode = newDestNode

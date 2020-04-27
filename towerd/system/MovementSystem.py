import math
import random

from towerd.System import System
from towerd.component.Movement import Movement
from towerd.component.MapNode import MapNode
from towerd.component.LocationCartesian import LocationCartesian
from towerd.util.EntityPoint2D import EntityPoint2D
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
            mapNodes = ecsManager.getComponentArr(MapNode)
            locComps = ecsManager.getComponentArr(LocationCartesian)

            # grab movement related details from the current entity
            movementComp = movementComps[entity.ID]
            speed = movementComp.speed
            fromEnt = movementComp.fromNode
            fromNode = mapNodes[movementComp.fromNode.ID]

            if not movementComp.destNode and fromNode.edges:
                destNodeEntity = random.choice(fromNode.edges)
                movementComp.destNode = destNodeEntity

            destEnt = movementComp.destNode
            destNode = mapNodes[destEnt.ID]

            # get the current location and target destination
            locComp = locComps[entity.ID]
            destLocComp = locComps[destEnt.ID]

            fromX, fromY = locComp.x, locComp.y
            destX, destY = destLocComp.x, destLocComp.y

            ep2d = EntityPoint2D(fromX, fromY, entity)
            state.dynamicTree = state.dynamicTree.remove(ep2d)

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

            ep2d = EntityPoint2D(locComp.x, locComp.y, entity)
            state.dynamicTree.add(ep2d)

            # If the entity is at the destination node, update to next destination node
            neighboringNodes = destNode.edges
            if locComp.x == destX and locComp.y == destY and neighboringNodes:
                newDestNode = random.choice(neighboringNodes)
                movementComp.destNode = newDestNode

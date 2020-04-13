import math

from ..System import System


class MovementSystem(System):
    def update(self, dt, state, movementComps, locComps):
        for entity in self.entities:
            movementComp = movementComps[entity.ID]
            speed = movementComp.speed
            fromNode = movementComp.fromNode
            destNode = movementComp.destNode

            m = state['map']
            fromNode = m.nodes[fromNode]
            destNode = m.nodes[destNode]
            locComp = locComps[entity.ID]

            fromX, fromY = locComp.x, locComp.y
            destX, destY = destNode.x, destNode.y

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
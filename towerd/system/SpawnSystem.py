from ..Map import Map, PathType

from towerd.System import System
from towerd.component.Attack import Attack
from towerd.component.Movement import Movement
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital

class SpawnSystem(System):
    def update(self, dt, state, ecs_manager):
        # Get path_start
        #TODO Not sure how to do this, need to get the info from Game
        pathStartX = 0
        pathStartY = 0

        # Get the number of mobs based on what wave it is
        #TODO Not sure how to do this, need to get the info from Game
        numMobs = 10

        # create the  mobs
        for i in range(numMobs):
            mob = self.ecsm.createEntity()

            self.ecsm.addEntityComponent(mob, LocationCartesian(pathStartX, pathStartY))
            self.ecsm.addEntityComponent(mob, Vital(100, 10))
            self.ecsm.addEntityComponent(mob, Movement(0.3, PathType.PATH_START.id, PathType.PATH_END.id))
            self.ecsm.addEntityComponent(mob, Attack(0.01, 2, 5, None, True))
            self.ecsm.addEntityComponent(mob, Faction(0))

            self.state['entities'][mob.ID] = mob
            setattr(self, f'e{i}', mob)
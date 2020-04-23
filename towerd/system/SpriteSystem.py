
from towerd.System import System
from towerd.component.Attack import Attack
from towerd.component.Movement import Movement
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital

from towerd.component.EntitySprite import EntitySprite


class SpriteSystem(System):
    def update(self, dt, state, ecs_manager):
        locComps = ecs_manager.getComponentArr(LocationCartesian)
        spriteComps = ecs_manager.getComponentArr(EntitySprite)


        # update locations for each entity
        for entity in self.entities:
            entityLocComp = locComps[entity.ID]

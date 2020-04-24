import pygame

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


        # update locations for each entity  - add all sprites to the group
        for entity in self.entities:
            entityLocComp = locComps[entity.ID]
            # locations
            EntitySprite.x = LocationCartesian.x
            EntitySprite.y = LocationCartesian.y

            # sprite groupings
            pygame.sprite.Group.add(spriteComps)



    def draw(self):
        """
        Method used to the groupings of sprites stored from update
        """
        pygame.sprite.draw()

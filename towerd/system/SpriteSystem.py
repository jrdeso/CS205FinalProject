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


        # update locations for each entity
        for entity in self.entities:
            entityLocComp = locComps[entity.ID]

            EntitySprite.x = LocationCartesian.x
            EntitySprite.y = LocationCartesian.y


    def draw(self, SpriteEntity):
        """
        Method used to draw a sprite
        :param SpriteEntity: Represents a sprite
        """

        # initialize sprite
        pygame.sprite.Sprite.__init__(SpriteEntity)

        image = pygame.Surface(SpriteEntity)  # Note: This could be where image is loaded from saved files
                                                    # See further pygame docs for info on how this is done
                                                # see EntitySprite for details-could load image there and use it here
        pygame.sprite.Sprite.update()


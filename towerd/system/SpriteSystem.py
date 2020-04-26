import pygame

from towerd.System import System
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Sprite import Sprite


class SpriteSystem(System):
    def __init__(self):
        super().__init__()
        self.entitySprite = {}

    def removeEntity(self, entity):
        del self.entitySprite[entity.ID]

    def update(self, dt, state, ecs_manager):
        locComps = ecs_manager.getComponentArr(LocationCartesian)
        spriteComps = ecs_manager.getComponentArr(Sprite)

        # update locations for each entity - add all sprites to the group
        for entity in self.entities:
            locComp = locComps[entity.ID]
            spriteComp = spriteComps[entity.ID]

            if entity.ID not in self.entitySprite:
                self.entitySprite[entity.ID] = EntitySprite(locComp.x, locComp.y, spriteComp.path)

            sprite = self.entitySprite[entity.ID]
            sprite.update(locComp.x, locComp.y)

    def drawSprites(self, screen):
        """
        Method used to the groupings of sprites stored from update
        """
        width, height = screen.get_size()
        for _, sprite in self.entitySprite.items():
            win_x = sprite.x/100 * width
            win_y = sprite.y/100 * height
            screen.blit(sprite.image, (win_x, win_y))


class EntitySprite(Sprite):
    def __init__(self, x, y, spritePath):
        self.x = x
        self.y = y

        self.spritePath = spritePath

        self.image = pygame.image.load(self.spritePath)
        self.rect = self.image.get_rect()
        # Note this may be where we also store on hand image file of sprite for use
        # could allow use for each entity to render through sprite system

    def update(self, x, y):
        self.x = x
        self.y = y

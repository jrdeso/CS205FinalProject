import dataclasses
import pygame


@dataclasses.dataclass
@pygame.sprite.Sprite
class EntitySprite:
    x: int
    y: int
    spritePath: str
    # Note this may be where we also store on hand image file of sprite for use
    # could allow use for each entity to render through sprite system
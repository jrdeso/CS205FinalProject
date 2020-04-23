import dataclasses
import pygame


@dataclasses.dataclass
@pygame.sprite.Sprite
class EntitySprite:
    x: int
    y: int
    spritePath: str

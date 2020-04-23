import dataclasses


@dataclasses.dataclass
class EntitySprite:
    x: int
    y: int
    spritePath: str

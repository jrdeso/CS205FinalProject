import dataclasses

from towerd.Entity import Entity


@dataclasses.dataclass
class Attack:
    attackRange: float
    attackSpeed: float
    dmg: float
    target: Entity

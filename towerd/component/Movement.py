import dataclasses

from towerd.Entity import Entity


@dataclasses.dataclass
class Movement:
    speed: float
    fromNode: Entity
    destNode: Entity

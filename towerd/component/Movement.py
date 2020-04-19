import dataclasses


@dataclasses.dataclass
class Movement:
    speed: float
    fromNode: int
    destNode: int

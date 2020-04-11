import dataclasses


@dataclasses.dataclass
class Upgrade:
    level: int
    upgradeCost: int

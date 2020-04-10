import dataclasses

from towerd.Entity import Entity
from towerd.util.packed_array import MappedPackedArray


class ComponentManager:
    def __init__(self, max_entities):
        self.components = {}
        self.component_arrs = []
        self.max_entities = max_entities

    def register(self, T):
        self.components[T.__name__] = len(self.component_arrs)
        self.component_arrs.append(MappedPackedArray(self.max_entities))

    def get_component_bits(self, T):
        bitshift = self.components[T.__name__]
        return 1 << bitshift

    def get_component_arr(self, T):
        return self.component_arrs[self.components[T.__name__]]

    def add_component(self, component, entity):
        idx = self.components[component.__class__.__name__]
        self.component_arrs[idx].append(component, key=entity.e_id)

    def remove_component(self, T, entity):
        idx = self.components[T.__name__]
        self.component_arrs[idx].remove_key(entity.e_id)

    def remove_all(self, entity):
        for arr in self.component_arrs:
            try:
                arr.remove_key(entity.e_id)
            except KeyError:
                continue


@dataclasses.dataclass
class LocNode:
    node: int


@dataclasses.dataclass
class LocCartesian:
    x: int
    y: int


@dataclasses.dataclass
class Level:
    level: int
    upgrade_cost: int


@dataclasses.dataclass
class Vital:
    health: int
    shield: int


@dataclasses.dataclass
class Movement:
    movement_speed: float
    from_node: int
    dest_node: int


@dataclasses.dataclass
class Attack:
    attack_range: float
    attack_speed: float
    dmg: float
    target: Entity


@dataclasses.dataclass
class Coin:
    value: int

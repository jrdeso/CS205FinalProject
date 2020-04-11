import dataclasses

from towerd.Entity import Entity
from towerd.util.packed_array import MappedPackedArray


class ComponentManager:
    """
    Manages all instances of registered components.

    :param max_entities: the maximum number of entities in the game

    :var components: a dictionary mapping the component name to its unique bitset
    :var component_arrs: an list of packed arrays of components
    :var max_entities: store of the max_entities parameter
    """
    def __init__(self, max_entities):
        self.components = {}
        self.component_arrs = []
        self.max_entities = max_entities

    def register(self, T):
        """
        Register a Component. Generates a unique bitset and adds it to the
        dictionary of components and associates a packed array with the
        component.

        :param T: the component class
        """
        self.components[T.__name__] = len(self.component_arrs)
        self.component_arrs.append(MappedPackedArray(self.max_entities))

    def get_component_bits(self, *Ts):
        """
        Get a bitset uniquely identifying the component class that are
        specified.

        :param Ts: any number of Component arguments
        """
        component_bits = 0
        for T in Ts:
            bitshift = self.components[T.__name__]
            component_bits |= 1 << bitshift
        return component_bits

    def get_component_arr(self, T):
        """
        Get a packed array of components associated with an entity.

        :param T: the Component class
        """
        return self.component_arrs[self.components[T.__name__]]

    def add_component(self, component, entity):
        """
        Associate an instance of a component with an entity.

        :param component: a component
        :param entity: the entity
        """
        idx = self.components[component.__class__.__name__]
        self.component_arrs[idx].append(component, key=entity.e_id)

    def remove_component(self, T, entity):
        """
        Remove components of type T with an entity.

        :param T: a Component
        :param entity: the entity
        """
        idx = self.components[T.__name__]
        self.component_arrs[idx].remove_key(entity.e_id)

    def remove_all(self, entity):
        """
        Remove all components associated with an entity

        :param entity: the entity
        """
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

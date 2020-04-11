import dataclasses

from towerd.Entity import Entity
from towerd.util.PackedArray import MappedPackedArray


class ComponentManager:
    """
    Manages all instances of registered components.

    :param max_entities: the maximum number of entities in the game

    :var components: a dictionary mapping the component name to its unique bitset
    :var component_arrs: an list of packed arrays of components
    :var max_entities: store of the max_entities parameter
    """
    def __init__(self, maxEntities):
        self.components = {}
        self.componentArrs = []
        self.maxEntities = maxEntities

    def register(self, T):
        """
        Register a Component. Generates a unique bitset and adds it to the
        dictionary of components and associates a packed array with the
        component.

        :param T: the component class
        """
        self.components[T.__name__] = len(self.componentArrs)
        self.componentArrs.append(MappedPackedArray(self.maxEntities))

    def getComponentBits(self, *Ts):
        """
        Get a bitset uniquely identifying the component class that are
        specified.

        :param Ts: any number of Component arguments
        """
        componentBits = 0
        for T in Ts:
            bitshift = self.components[T.__name__]
            componentBits |= 1 << bitshift
        return componentBits

    def getComponentArr(self, T):
        """
        Get a packed array of components associated with an entity.

        :param T: the Component class
        """
        return self.componentArrs[self.components[T.__name__]]

    def addComponent(self, component, entity):
        """
        Associate an instance of a component with an entity.

        :param component: a component
        :param entity: the entity
        """
        idx = self.components[component.__class__.__name__]
        self.componentArrs[idx].append(component, key=entity.ID)

    def removeComponent(self, T, entity):
        """
        Remove components of type T with an entity.

        :param T: a Component
        :param entity: the entity
        """
        idx = self.components[T.__name__]
        self.componentArrs[idx].removeKey(entity.ID)

    def removeAll(self, entity):
        """
        Remove all components associated with an entity

        :param entity: the entity
        """
        for arr in self.componentArrs:
            try:
                arr.removeKey(entity.ID)
            except KeyError:
                continue


@dataclasses.dataclass
class LocationNode:
    node: int


@dataclasses.dataclass
class LocationCartesian:
    x: int
    y: int


@dataclasses.dataclass
class Level:
    level: int
    upgradeCost: int


@dataclasses.dataclass
class Vital:
    health: int
    shield: int


@dataclasses.dataclass
class Movement:
    speed: float
    fromNode: int
    destNode: int


@dataclasses.dataclass
class Attack:
    attackRange: float
    attackSpeed: float
    dmg: float
    target: Entity


@dataclasses.dataclass
class Coin:
    value: int

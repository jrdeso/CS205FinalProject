import abc
import math


class System(abc.ABC):
    """
    A system consisting of the entities that it needs to update.

    :var entities: all the entities the system needs to update
    """
    def __init__(self):
        self.entities = set()

    def removeEntity(self, entity):
        pass

    @abc.abstractmethod
    def update(self, dt, state, ecs_manager):
        """
        Perform an update across all entities.

        :param dt: the amount of time passed since the last update
        :param state: the game state
        :param ecs_manager: a ECSManager for retrieving entity data
        """
        raise NotImplementedError


class SystemManager:
    """
    Manages all instances of registered systems

    :var systems: a dictionary mapping the system name to an instance of the
        system
    :var system_bits: a dictionary mapping the system name to a bitset
        representing required components
    :var max_entities: store of the max_entities parameter
    """
    def __init__(self):
        self.systems = {}
        self.systemBits = {}

    def register(self, T, bitset):
        """
        Register a System. Associates a bitset representing required components
        to the system.

        :param T: the System class
        :param bitset: a bitset representing required components
        """
        self.systems[T.__name__] = T()
        self.systemBits[T.__name__] = bitset

    def get(self, T):
        """
        Get the instance of the System.

        :param T: the System class
        """
        return self.systems[T.__name__]

    def removeEntity(self, T, entity):
        """
        Remove an entity from a registered System.

        :param T: the System class
        :param entity: the entity to remove
        """
        self.systems[T.__name__].entities.discard(entity)
        self.systems[T.__name__].removeEntity(entity)

    def removeEntityAll(self, entity):
        """
        Remove an entity from all systems.

        :param T: the System class
        :param entity: the entity to remove
        """
        for system in self.systems.values():
            system.entities.discard(entity)
            system.removeEntity(entity)

    def updateEntity(self, entity, entityBitset):
        """
        Update an entity bitset. Remove enitity from systems where the entity
        bitset in part does not match the system bitset. Add them to systems
        where the entity_bitset does in part match the system bitset.

        :param entity: the entity
        :param entityBitset: the new bitset for the entity
        """
        for system in self.systems.values():
            systemBits = self.systemBits[system.__class__.__name__]
            if systemBits & entityBitset == systemBits:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)

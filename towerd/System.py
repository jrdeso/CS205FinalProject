import abc


class System(abc.ABC):
    def __init__(self):
        self.entities = set()

    @abc.abstractmethod
    def update(self, state):
        raise NotImplementedError


class SystemManager:
    def __init__(self):
        self.systems = {}
        self.system_bits = {}

    def register(self, T, bitset):
        self.systems[T.__name__] = T()
        self.system_bits[T.__name__] = bitset

    def remove_system_entity(self, entity):
        for system in self.systems.value():
            system.entities.discard(entity)

    def update_system_entity(self, entity, entity_bitset):
        for system in self.systems.values():
            system_bitset = self.system_bitset[system.__class__.__name__]
            if system_bitset & entity_bitset == entity_bitset:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)

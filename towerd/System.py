import abc
import math


class System(abc.ABC):
    def __init__(self):
        self.entities = set()

    @abc.abstractmethod
    def update(self, state, *args, **kwargs):
        raise NotImplementedError


class SystemManager:
    def __init__(self):
        self.systems = {}
        self.system_bits = {}

    def register(self, T, bitset):
        self.systems[T.__name__] = T()
        self.system_bits[T.__name__] = bitset

    def remove_system_entity(self, entity):
        for system in self.systems.values():
            system.entities.discard(entity)

    def update_system_entity(self, entity, entity_bitset):
        for system in self.systems.values():
            system_bits = self.system_bits[system.__class__.__name__]
            print(bin(system_bits), bin(entity_bitset))
            if system_bits & entity_bitset == system_bits:
                system.entities.add(entity)
            else:
                system.entities.discard(entity)

import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Entity:
    e_id: int


class EntityManager:
    def __init__(self, max_entities):
        self.available = collections.deque(range(max_entities))
        self.bitsets = list((None,) * max_entities)
        self.n_active = 0

    def create_entity(self):
        self.n_active += 1
        e_id = self.available.popleft()
        return Entity(e_id)

    def remove_entity(self, entity):
        self.bitsets[entity.e_id] = 0
        self.available.append(entity.e_id)
        self.n_active -= 1

    def change_bitset(self, entity, bitset):
        if entity.e_id > len(self.bitsets):
            raise ValueError('Entity ID is greater than max_entities')
        self.bitsets[entity.e_id] = bitset

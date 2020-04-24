import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Entity:
    ID: int


class EntityManager:
    def __init__(self, maxEntities):
        self.available = collections.deque(range(maxEntities))
        self.bitsets = list((0,) * maxEntities)
        self.nActive = 0

    def create(self):
        eId = self.available.popleft()
        self.nActive += 1
        return Entity(eId)

    def remove(self, entity):
        self.bitsets[entity.ID] = 0
        self.available.append(entity.ID)
        self.nActive -= 1

    def getBitset(self, entity):
        return self.bitsets[entity.ID]

    def updateBitset(self, entity, bitset):
        if entity.ID > len(self.bitsets):
            raise ValueError('Entity ID is greater than max_entities')
        self.bitsets[entity.ID] = bitset

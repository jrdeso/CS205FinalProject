import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Entity:
    ID: int


class EntityManager:
    def __init__(self, maxEntities):
        self.available = collections.deque(range(maxEntities))
        self.bitsets = list((None,) * maxEntities)
        self.nActive = 0

    def createEntity(self):
        self.nActive += 1
        eId = self.available.popleft()
        return Entity(eId)

    def removeEntity(self, entity):
        self.bitsets[entity.ID] = 0
        self.available.append(entity.ID)
        self.nActive -= 1

    def updateBitset(self, entity, bitset):
        if entity.ID > len(self.bitsets):
            raise ValueError('Entity ID is greater than max_entities')
        self.bitsets[entity.ID] = bitset

from towerd.Entity import EntityManager
from towerd.Component import ComponentManager
from towerd.System import SystemManager


class ECSManager:
    def __init__(self, maxEntities):
        self.em = EntityManager(maxEntities)
        self.cm = ComponentManager(maxEntities)
        self.sm = SystemManager()

        self.createEntity = self.em.create
        self.getEntityBitset = self.em.getBitset

        self.registerComponent = self.cm.register
        self.getComponentBits = self.cm.getBitset
        self.getComponentArr = self.cm.getArr

        self.getSystem = self.sm.get

    def addEntityComponent(self, entity, component):
        entityBitset = self.em.getBitset(entity)
        entityBitset |= self.cm.getBitset(component.__class__)

        self.em.updateBitset(entity, entityBitset)
        self.cm.add(component, entity)
        self.sm.updateEntity(entity, entityBitset)

    def removeEntityComponent(self, entity, C):
        self.cm.removeComponent(C, entity)

        componentBitset = self.cm.getBitset(C)
        entityBitset = self.em.getBitset(entity)
        entityBitset ^= componentBitset

        self.em.updateBitset(entity, entityBitset)
        self.sm.updateSystemEntity(entity, entityBitset)

    def getEntityComponent(self, entity, C):
        componentArr = self.cm.getArr(C)
        return componentArr[entity.ID]

    def removeEntity(self, entity):
        self.cm.removeEntityAll(entity)
        self.sm.removeEntityAll(entity)
        self.em.remove(entity)

    def registerSystem(self, S, *Cs):
        systemBits = 0
        for C in Cs:
            componentBits = self.cm.getBitset(C)
            systemBits |= componentBits
        self.sm.register(S, systemBits)

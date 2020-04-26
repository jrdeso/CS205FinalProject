from towerd.System import System
from towerd.component.Vital import Vital

class RemoveDeadEntitiesDamage(System):
    def update(self, dt, state, ecsManager):
        for entity in self.entities:
            vitalComps = ecsManager.getComponentArr(Vital)
            if(vitalComps.health <= 0):
                # The entity is dead, remove it from self.entites
                self.entities.remove(entity)

                # Remove the entity from ecs mananger
                ecsManager.removeEntity(entity)
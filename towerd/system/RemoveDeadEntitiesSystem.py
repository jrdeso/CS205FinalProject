from towerd.System import System
from towerd.component.Vital import Vital
from towerd.component.LocationCartesian import LocationCartesian
from towerd.util.EntityPoint2D import EntityPoint2D


class RemoveDeadEntitiesSystem(System):
    def update(self, dt, state, ecsManager):
        entities = set(self.entities)
        locComps = ecsManager.getComponentArr(LocationCartesian)
        vitalComps = ecsManager.getComponentArr(Vital)

        for entity in entities:
            try:
                locComp = locComps[entity.ID]
                vitalComp = vitalComps[entity.ID]
            except KeyError:
                continue

            if vitalComp.health <= 0:
                # The entity is dead, remove it from self.entites
                self.entities.remove(entity)

                # Remove the entity from ecs mananger
                ecsManager.removeEntity(entity)

                ep2d = EntityPoint2D(locComp.x, locComp.y, entity)
                state.dynamicTree = state.dynamicTree.remove(ep2d)

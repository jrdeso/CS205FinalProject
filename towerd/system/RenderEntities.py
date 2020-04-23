#import pygame_gui

from towerd.System import System
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital


class RenderEntities(System):
    def update(self, dt, state, ecs_manager):
        factionComps = ecs_manager.getComponentArr(Faction)
        locComps = ecs_manager.getComponentArr(LocationCartesian)
        vitalComps = ecs_manager.getComponentArr(Vital)



from towerd.System import System
from towerd.component.Attack import Attack
from towerd.component.Faction import Faction
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.Vital import Vital


class SpriteSystem(System):
    def update(self, dt, state, ecs_manager):

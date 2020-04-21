import unittest

from ..Entity import Entity
from ..Component import ComponentManager
from ..component.LocationCartesian import LocationCartesian
from ..component.Vital import Vital


class TestComponentManager(unittest.TestCase):
    def setUp(self):
        self.cm = ComponentManager(5)

    def test_component_manager(self):
        self.cm.register(LocationCartesian)
        self.cm.register(Vital)

        self.assertEqual(self.cm.getBitset(LocationCartesian), 1)
        self.assertEqual(self.cm.getBitset(Vital), 2)

        ent = Entity(1)
        pos = LocationCartesian(1, 1)
        vit = Vital(100, 10)

        self.cm.add(pos, ent)
        self.cm.add(vit, ent)

        loc_mpa = self.cm.getArr(LocationCartesian)
        self.assertEqual(pos, loc_mpa[ent.ID])

        self.cm.removeEntityAll(ent)
        self.assertEqual(len(self.cm.getArr(LocationCartesian)), 0)
        self.assertEqual(len(self.cm.getArr(Vital)), 0)

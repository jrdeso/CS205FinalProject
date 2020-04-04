import unittest

from ..Entity import Entity
from ..Components import ComponentManager, LocCartesian, Vital


class TestComponentManager(unittest.TestCase):
    def setUp(self):
        self.cm = ComponentManager(5)

    def test_component_manager(self):
        self.cm.register(LocCartesian)
        self.cm.register(Vital)

        self.assertEqual(self.cm.get_component_bits(LocCartesian), 1)
        self.assertEqual(self.cm.get_component_bits(Vital), 2)

        ent = Entity(1)
        pos = LocCartesian(1, 1)
        vit = Vital(100, 10)

        self.cm.add_component(pos, ent)
        self.cm.add_component(vit, ent)

        loc_mpa = self.cm.get_component_arr(LocCartesian)
        self.assertEqual(pos, loc_mpa[ent.e_id])

        self.cm.remove_all(ent)
        self.assertEqual(len(self.cm.get_component_arr(LocCartesian)), 0)
        self.assertEqual(len(self.cm.get_component_arr(Vital)), 0)

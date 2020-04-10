import unittest

from ..Entity import Entity
from ..System import SystemManager, MovementSystem


class TestSystemManager(unittest.TestCase):
    def setUp(self):
        self.sm = SystemManager()

    def test_system_manager(self):
        self.sm.register(MovementSystem, 1)

        ms = self.sm.systems[MovementSystem.__name__]
        ms_bits = self.sm.system_bits[MovementSystem.__name__]
        self.assertEqual(ms_bits, 1)

        ent = Entity(1)

        self.sm.update_system_entity(ent, 10)
        self.assertEquals(len(ms.entities), 0)

        self.sm.update_system_entity(ent, 33)
        self.assertEquals(len(ms.entities), 1)

        self.sm.remove_system_entity(ent)
        self.assertEquals(len(ms.entities), 0)

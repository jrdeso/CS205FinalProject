import unittest

from ..Entity import Entity
from ..System import SystemManager
from ..system.MovementSystem import MovementSystem


class TestSystemManager(unittest.TestCase):
    def setUp(self):
        self.sm = SystemManager()

    def test_system_manager(self):
        self.sm.register(MovementSystem, 1)

        ms = self.sm.systems[MovementSystem.__name__]
        ms_bits = self.sm.systemBits[MovementSystem.__name__]
        self.assertEqual(ms_bits, 1)

        ent = Entity(1)

        self.sm.updateSystemEntity(ent, 10)
        self.assertEqual(len(ms.entities), 0)

        self.sm.updateSystemEntity(ent, 33)
        self.assertEqual(len(ms.entities), 1)

        self.sm.removeSystemEntity(MovementSystem, ent)
        self.assertEqual(len(ms.entities), 0)

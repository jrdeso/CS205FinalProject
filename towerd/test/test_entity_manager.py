import unittest

from ..Entity import EntityManager


class TestEntityManager(unittest.TestCase):
    def setUp(self):
        self.em = EntityManager(5)

    def test_entity_manager(self):
        ent = self.em.createEntity()

        self.em.updateBitset(ent, 20)
        self.assertEqual(self.em.bitsets[ent.ID], 20)

        e_id = ent.ID
        self.em.removeEntity(ent)
        self.assertEqual(self.em.available[-1], e_id)

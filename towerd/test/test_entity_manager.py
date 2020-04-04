import unittest

from ..Entity import EntityManager


class TestEntityManager(unittest.TestCase):
    def setUp(self):
        self.em = EntityManager(5)

    def test_entity_manager(self):
        ent = self.em.create_entity()

        self.em.change_bitset(ent, 20)
        self.assertEqual(self.em.bitsets[ent.e_id], 20)

        e_id = ent.e_id
        self.em.remove_entity(ent)
        self.assertEqual(self.em.available[-1], e_id)

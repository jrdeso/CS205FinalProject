import kdtree
import random
import unittest

from ..util.EntityPoint2D import EntityPoint2D


class TestKDTree(unittest.TestCase):
    def setUp(self):
        self.k2 = kdtree.create(dimensions=2)
        for x in range(10):
            for y in range(10):
                self.k2.add(EntityPoint2D(x/10, y/10, entities=[x, y]))

    def test_search_point(self):
        eps = [node.data for node, _ in self.k2.search_knn((0.2, 0.2), 3)]

        entities = []
        for ep in eps:
            entities.extend(ep.entities)

        self.assertEqual(set(entities), set([2, 3]))

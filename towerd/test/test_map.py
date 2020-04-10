import unittest

from ..Map import Map, MapNode, PathType


class TestMap(unittest.TestCase):
    def test_map(self):
        m = Map()
        n1 = m.addNode(PathType.PATH_START, 0, 0)
        n2 = m.addNode(PathType.PATH, 1, 0)
        n3 = m.addNode(PathType.PATH_END, 2, 0)

        m.addEdge(n1, n3)
        m.addEdge(n2, n3)

        self.assertTrue(m.existsEdge(n1, n3))
        self.assertFalse(m.existsEdge(n1, n2))

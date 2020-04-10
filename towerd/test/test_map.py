import json
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
        self.assertFalse(m.existsEdge(n3, n1))
        self.assertFalse(m.existsEdge(n1, n2))

    def test_generate(self):
        jsonstr = '{"0":{"type":"path_start","coord":[0.0,0.05],"edges":["1"]},"1":{"type":"path_end","coord":[0.1,0.15],"edges":[]}}'
        map_json = json.loads(jsonstr)

        m = Map(map_json=map_json)
        self.assertTrue(m.existsEdge(0, 1))
        self.assertFalse(m.existsEdge(1, 0))

        self.assertEqual(m.nodes[0].pathType, PathType.PATH_START)
        self.assertEqual(m.nodes[0].x, 0.0)
        self.assertEqual(m.nodes[0].y, 0.05)

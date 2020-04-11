import unittest

from ..Entity import EntityManager
from ..Component import ComponentManager, LocationCartesian, Movement, Vital
from ..System import SystemManager
from ..system.MovementSystem import MovementSystem
from ..Map import Map, PathType


class TestECS(unittest.TestCase):
    def setUp(self):
        self.map = Map()
        n1 = self.map.addNode(PathType.PATH_START, 0.15, 0.2)
        n2 = self.map.addNode(PathType.PATH_END, 0.9, 0.2)
        self.map.addEdge(n1, n2)

        self.state = {}
        self.state['map'] = self.map
        self.state['entities'] = {}

        # Initial ECS setup
        self.em = EntityManager(5)

        self.cm = ComponentManager(5)
        self.cm.register(LocationCartesian)
        self.cm.register(Movement)
        self.cm.register(Vital)

        mob_bits = self.cm.getComponentBits(LocationCartesian, Movement, Vital)

        self.sm = SystemManager()
        self.sm.register(MovementSystem, mob_bits)

        # Make mobs
        self.orig_coords = [(0.15, 0.2)]
        for i in range(len(self.orig_coords)):
            ent = self.em.createEntity()
            self.state['entities'][ent.ID] = ent
            self.em.updateBitset(ent, mob_bits)

            loc = LocationCartesian(*self.orig_coords[i])
            vit = Vital(100, 10)
            movement = Movement(0.3, n1.id, n2.id)

            self.cm.addComponent(loc, ent)
            self.cm.addComponent(vit, ent)
            self.cm.addComponent(movement, ent)

            self.sm.updateSystemEntity(ent, mob_bits)

    def test_ecs(self):
        ms = self.sm.getSystem(MovementSystem)
        ms.update(1, self.state, self.cm.getComponentArr(Movement),
                  self.cm.getComponentArr(LocationCartesian))

        # Won't need to do any of the below in Game class
        e0 = self.state['entities'][0]

        loc_comps = self.cm.getComponentArr(LocationCartesian)
        movements = self.cm.getComponentArr(Movement)

        loc_comp0 = loc_comps[e0.ID]
        movement0 = movements[e0.ID]

        orig_coords0 = self.orig_coords[0]
        self.assertEqual(loc_comp0.x, orig_coords0[0] + movement0.speed)
        self.assertEqual(loc_comp0.y, orig_coords0[1])

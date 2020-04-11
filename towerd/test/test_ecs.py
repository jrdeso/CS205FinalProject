import unittest

from ..Entity import EntityManager
from ..Components import ComponentManager, LocCartesian, Movement, Vital
from ..System import SystemManager, MovementSystem
from ..Map import Map, PathType


class TestECS(unittest.TestCase):
    def setUp(self):
        self.em = EntityManager(5)

        self.cm = ComponentManager(5)
        self.cm.register(LocCartesian)
        self.cm.register(Movement)
        self.cm.register(Vital)

        loc_cartesian_bits = self.cm.get_component_bits(LocCartesian)
        movement_bits = self.cm.get_component_bits(Movement)
        vital_bits = self.cm.get_component_bits(Vital)

        mob_bits = loc_cartesian_bits | movement_bits | vital_bits

        self.sm = SystemManager()
        self.sm.register(MovementSystem, loc_cartesian_bits | movement_bits)

        self.map = Map()
        n1 = self.map.addNode(PathType.PATH_START, 0.15, 0.2)
        n2 = self.map.addNode(PathType.PATH_END, 0.9, 0.2)
        self.map.addEdge(n1, n2)

        self.state = {}
        self.state['map'] = self.map
        self.state['entities'] = {}

        # Make mobs
        self.orig_coords = [(0.15, 0.2)]
        for i in range(len(self.orig_coords)):
            ent = self.em.create_entity()
            self.state['entities'][ent.e_id] = ent
            self.em.change_bitset(ent, mob_bits)

            loc = LocCartesian(*self.orig_coords[i])
            vit = Vital(100, 10)
            movement = Movement(0.3, n1.id, n2.id)

            self.cm.add_component(loc, ent)
            self.cm.add_component(vit, ent)
            self.cm.add_component(movement, ent)

            self.sm.update_system_entity(ent, mob_bits)

    def test_ecs(self):
        ms = self.sm.systems[MovementSystem.__name__]
        ms.update(1, self.state, self.cm.get_component_arr(Movement),
                  self.cm.get_component_arr(LocCartesian))

        # Won't need to do any of the below in Game class
        e0 = self.state['entities'][0]

        loc_comps = self.cm.get_component_arr(LocCartesian)
        movements = self.cm.get_component_arr(Movement)

        loc_comp0 = loc_comps[e0.e_id]
        movement0 = movements[e0.e_id]

        orig_coords0 = self.orig_coords[0]
        self.assertEquals(loc_comp0.x, orig_coords0[0] + movement0.movement_speed)
        self.assertEquals(loc_comp0.y, orig_coords0[1])

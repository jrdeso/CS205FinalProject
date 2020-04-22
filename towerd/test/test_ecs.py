import unittest

import kdtree

from ..ECS import ECSManager
from ..util.EntityPoint2D import EntityPoint2D
from ..component.LocationCartesian import LocationCartesian
from ..component.LocationNode import LocationNode
from ..component.Movement import Movement
from ..component.Vital import Vital
from ..component.Attack import Attack
from ..component.Faction import Faction
from ..system.MovementSystem import MovementSystem
from ..system.AttackSystem import AttackSystem
from ..Map import Map, PathType


class TestECS(unittest.TestCase):
    def setUp(self):
        self.map = Map()
        n1 = self.map.addNode(PathType.PATH_START, 0.15, 0.2)
        n2 = self.map.addNode(PathType.PATH_END, 0.9, 0.2)
        n3 = self.map.addNode(PathType.TOWER, 0.2, 0.1)
        self.map.addEdge(n1, n2)

        self.state = {}
        self.state['map'] = self.map
        self.state['entities'] = {}

        # Initial ECS setup
        self.ecsm = ECSManager(5)
        self.ecsm.registerComponent(LocationCartesian)
        self.ecsm.registerComponent(LocationNode)
        self.ecsm.registerComponent(Movement)
        self.ecsm.registerComponent(Vital)
        self.ecsm.registerComponent(Attack)
        self.ecsm.registerComponent(Faction)

        self.ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        self.ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)

        # Make mobs
        self.orig_coords = [(0.15, 0.2), (0.2, 0.2)]
        for i in range(len(self.orig_coords)):
            ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(ent, LocationCartesian(*self.orig_coords[i]))
            self.ecsm.addEntityComponent(ent, Vital(100, 10))
            self.ecsm.addEntityComponent(ent, Movement(0.3, n1.id, n2.id))
            self.ecsm.addEntityComponent(ent, Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True))
            self.ecsm.addEntityComponent(ent, Faction(faction=0))

            self.state['entities'][ent.ID] = ent
            setattr(self, f'e{i}', ent)

        # Make tower
        tower_node = n3
        tower_ent = self.ecsm.createEntity()
        self.ecsm.addEntityComponent(tower_ent, LocationNode(tower_node.id))
        self.ecsm.addEntityComponent(tower_ent, LocationCartesian(tower_node.x, tower_node.y))
        self.ecsm.addEntityComponent(tower_ent, Attack(attackRange=0.5, attackSpeed=2, dmg=5, target=None, attackable=False))
        self.ecsm.addEntityComponent(tower_ent, Faction(faction=1))

        self.state['entities'][tower_ent.ID] = tower_ent

        # build tree
        k2tree = kdtree.create(dimensions=2)
        k2tree.add(EntityPoint2D(*self.orig_coords[0], entity=self.state['entities'][0]))
        k2tree.add(EntityPoint2D(tower_node.x, tower_node.y, entity=tower_ent))
        self.state['tree'] = k2tree

    def test_movement(self):
        ms = self.ecsm.getSystem(MovementSystem)
        ms.update(1, self.state, self.ecsm)

        # Won't need to do any of the below in Game class
        loc_comp0 = self.ecsm.getEntityComponent(self.e0, LocationCartesian)
        movement0 = self.ecsm.getEntityComponent(self.e0, Movement)

        orig_coords0 = self.orig_coords[0]
        self.assertEqual(loc_comp0.x, orig_coords0[0] + movement0.speed)
        self.assertEqual(loc_comp0.y, orig_coords0[1])

    def test_attack(self):
        atks = self.ecsm.getSystem(AttackSystem)
        atks.update(1, self.state, self.ecsm)
        atks.update(1, self.state, self.ecsm)

        vital_comp0 = self.ecsm.getEntityComponent(self.e0, Vital)
        vital_comp1 = self.ecsm.getEntityComponent(self.e1, Vital)

        self.assertEqual(vital_comp0.health, 100)
        self.assertEqual(vital_comp0.shield, 0)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

        atks.update(1, self.state, self.ecsm)
        self.assertEqual(vital_comp0.health, 90)
        self.assertEqual(vital_comp0.shield, 0)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

import unittest

import kdtree

from ..Entity import EntityManager
from ..util.EntityPoint2D import EntityPoint2D
from ..Component import ComponentManager
from ..component.LocationCartesian import LocationCartesian
from ..component.LocationNode import LocationNode
from ..component.Movement import Movement
from ..component.Vital import Vital
from ..component.Attack import Attack
from ..component.Faction import Faction
from ..System import SystemManager
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
        self.em = EntityManager(5)

        self.cm = ComponentManager(5)
        self.cm.register(LocationCartesian)
        self.cm.register(LocationNode)
        self.cm.register(Movement)
        self.cm.register(Vital)
        self.cm.register(Attack)
        self.cm.register(Faction)

        mob_bits = self.cm.getComponentBits(LocationCartesian, Movement, Vital, Attack, Faction)
        attack_system_bits = self.cm.getComponentBits(Attack, Faction, LocationCartesian)

        self.sm = SystemManager()
        self.sm.register(MovementSystem, mob_bits)
        self.sm.register(AttackSystem, attack_system_bits)

        # Make mobs
        self.orig_coords = [(0.15, 0.2), (0.2, 0.2)]
        for i in range(len(self.orig_coords)):
            ent = self.em.createEntity()
            self.state['entities'][ent.ID] = ent
            self.em.updateBitset(ent, mob_bits)

            loc = LocationCartesian(*self.orig_coords[i])
            vit = Vital(100, 10)
            movement = Movement(0.3, n1.id, n2.id)
            attack = Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True)
            faction = Faction(faction=0)

            self.cm.addComponent(loc, ent)
            self.cm.addComponent(vit, ent)
            self.cm.addComponent(movement, ent)
            self.cm.addComponent(attack, ent)
            self.cm.addComponent(faction, ent)

            self.sm.updateSystemEntity(ent, mob_bits)
            setattr(self, f'e{i}', ent)

        # Make tower
        tower_bits = self.cm.getComponentBits(LocationNode, LocationCartesian, Attack, Faction)
        tower_ent = self.em.createEntity()
        self.state['entities'][tower_ent.ID] = tower_ent
        self.em.updateBitset(tower_ent, tower_bits)

        tower_node = n3
        loc_node = LocationNode(tower_node.id)
        loc_cart = LocationCartesian(tower_node.x, tower_node.y)
        attack = Attack(attackRange=0.5, attackSpeed=2, dmg=5, target=None, attackable=False)
        faction = Faction(faction=1)

        self.cm.addComponent(loc_node, tower_ent)
        self.cm.addComponent(loc_cart, tower_ent)
        self.cm.addComponent(attack, tower_ent)
        self.cm.addComponent(faction, tower_ent)

        self.sm.updateSystemEntity(tower_ent, tower_bits)

        # build tree
        k2tree = kdtree.create(dimensions=2)
        k2tree.add(EntityPoint2D(*self.orig_coords[0], entity=self.state['entities'][0]))
        k2tree.add(EntityPoint2D(tower_node.x, tower_node.y, entity=tower_ent))
        self.state['tree'] = k2tree

    def test_movement(self):
        ms = self.sm.getSystem(MovementSystem)
        ms.update(1, self.state, self.cm)

        # Won't need to do any of the below in Game class
        loc_comps = self.cm.getComponentArr(LocationCartesian)
        movements = self.cm.getComponentArr(Movement)

        loc_comp0 = loc_comps[self.e0.ID]
        movement0 = movements[self.e0.ID]

        orig_coords0 = self.orig_coords[0]
        self.assertEqual(loc_comp0.x, orig_coords0[0] + movement0.speed)
        self.assertEqual(loc_comp0.y, orig_coords0[1])

    def test_attack(self):
        atks = self.sm.getSystem(AttackSystem)
        atks.update(1, self.state, self.cm)
        atks.update(1, self.state, self.cm)

        vital_comps = self.cm.getComponentArr(Vital)
        vital_comp0 = vital_comps[self.e0.ID]
        vital_comp1 = vital_comps[self.e1.ID]

        self.assertEqual(vital_comp0.health, 100)
        self.assertEqual(vital_comp0.shield, 0)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

        atks.update(1, self.state, self.cm)
        self.assertEqual(vital_comp0.health, 90)
        self.assertEqual(vital_comp0.shield, 0)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

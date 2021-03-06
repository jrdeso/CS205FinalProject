import unittest

import kdtree

from ..Game import GameState
from ..ECS import ECSManager
from ..util.EntityPoint2D import EntityPoint2D
from ..component.LocationCartesian import LocationCartesian
from ..component.MapNode import MapNode, PathType
from ..component.Movement import Movement
from ..component.Vital import Vital
from ..component.Attack import Attack
from ..component.Faction import Faction
from ..component.Coin import Coin
from ..system.MovementSystem import MovementSystem
from ..system.AttackSystem import AttackSystem
from ..system.SpawnSystem import SpawnSystem
from ..system.PlayerDamage import PlayerDamage


class TestECS(unittest.TestCase):
    def setUp(self):
        state = GameState()
        state.wave = 0
        state.entities = {}
        state.dynamicTree = kdtree.create(dimensions=2)
        state.staticTree = kdtree.create(dimensions=2)

        # Initial ECS setup
        self.maxEntities = 20
        ecsm = ECSManager(self.maxEntities)
        ecsm.registerComponent(Coin)
        ecsm.registerComponent(LocationCartesian)
        ecsm.registerComponent(MapNode)
        ecsm.registerComponent(Movement)
        ecsm.registerComponent(Vital)
        ecsm.registerComponent(Attack)
        ecsm.registerComponent(Faction)

        ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)
        ecsm.registerSystem(SpawnSystem, MapNode, LocationCartesian)
        ecsm.registerSystem(PlayerDamage, Faction, LocationCartesian, Attack, Vital)

        ents = [ecsm.createEntity() for i in range(3)]
        mapObj = [
                (PathType.PATH_START, (15, 20), [1]),
                (PathType.PATH, (20, 20), [2]),
                (PathType.PATH_END, (20, 70), []),
                ]

        for i, (ent, obj) in enumerate(zip(ents, mapObj)):
            pathType, coords, edges = obj
            pathType = PathType.GetEnum(pathType)
            edges = [ents[int(e)] for e in edges]
            ecsm.addEntityComponent(ent, LocationCartesian(*coords))
            ecsm.addEntityComponent(ent, MapNode(pathType, edges))
            state.mapEntities[ent.ID] = ent
            setattr(self, f'n{i}', ent)

        player = ecsm.createEntity()
        ecsm.addEntityComponent(player, Vital(100, 0))
        ecsm.addEntityComponent(player, Coin(100))
        ecsm.addEntityComponent(player, Faction(1))
        state.player = player

        # Make mobs
        self.orig_coords = [(15, 20), (20, 20)]
        for i in range(len(self.orig_coords)):
            ent = ecsm.createEntity()
            ecsm.addEntityComponent(ent, LocationCartesian(*self.orig_coords[i]))
            ecsm.addEntityComponent(ent, Vital(100, 10))
            ecsm.addEntityComponent(ent, Movement(30, self.n0, self.n1))
            ecsm.addEntityComponent(ent, Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True))
            ecsm.addEntityComponent(ent, Faction(faction=0))

            state.dynamicTree.add(EntityPoint2D(*self.orig_coords[0], entity=ent))
            state.entities[ent.ID] = ent
            setattr(self, f'e{i}', ent)

        # Make tower
        mapLoc = ecsm.getEntityComponent(self.n2, LocationCartesian)
        tower_ent = ecsm.createEntity()
        ecsm.addEntityComponent(tower_ent, LocationCartesian(mapLoc.x, mapLoc.y))
        ecsm.addEntityComponent(tower_ent, Attack(attackRange=50, attackSpeed=2, dmg=5, target=None, attackable=False))
        ecsm.addEntityComponent(tower_ent, Faction(faction=1))

        state.entities[tower_ent.ID] = tower_ent

        # build tree
        state.staticTree.add(EntityPoint2D(mapLoc.x, mapLoc.y, entity=tower_ent))

        self.state = state
        self.ecsm = ecsm

    def test_movement(self):
        ms = self.ecsm.getSystem(MovementSystem)
        ms.update(1, self.state, self.ecsm)

        # Won't need to do any of the below in Game class
        loc_comp0 = self.ecsm.getEntityComponent(self.e0, LocationCartesian)
        movement0 = self.ecsm.getEntityComponent(self.e0, Movement)

        orig_coords0 = [-10, 20]
        self.assertEqual(loc_comp0.x, orig_coords0[0] + movement0.speed)
        self.assertEqual(loc_comp0.y, orig_coords0[1])

    def test_attack(self):
        atks = self.ecsm.getSystem(AttackSystem)
        atks.update(1, self.state, self.ecsm)
        atks.update(1, self.state, self.ecsm)

        vital_comp0 = self.ecsm.getEntityComponent(self.e0, Vital)
        vital_comp1 = self.ecsm.getEntityComponent(self.e1, Vital)

        self.assertEqual(vital_comp0.health, 100)
        self.assertEqual(vital_comp0.shield, 10)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

        atks.update(1, self.state, self.ecsm)
        self.assertEqual(vital_comp0.health, 100)
        self.assertEqual(vital_comp0.shield, 10)
        self.assertEqual(vital_comp1.health, 100)
        self.assertEqual(vital_comp1.shield, 10)

    def test_spawn(self):
        ss = self.ecsm.getSystem(SpawnSystem)

        self.state.wave = 1
        ss.update(0, self.state, self.ecsm)
        self.state.waveInProgress = True

        self.assertEqual(self.ecsm.em.nActive, 7)

        for i in range(23, self.maxEntities):
            locComp = self.ecsm.getEntityComponent(self.state.entities[i], LocationCartesian)
            moveComp = self.ecsm.getEntityComponent(self.state.entities[i], Movement)

            mapLoc = self.ecsm.getEntityComponent(self.n0, LocationCartesian)
            locComp.x = 15
            self.assertEqual(mapLoc.x, locComp.x)
            self.assertEqual(mapLoc.y, locComp.y)
            self.assertEqual(self.n0, moveComp.fromNode)
            self.assertEqual(self.n1, moveComp.destNode)

    def test_damage(self):
        pd = self.ecsm.getSystem(PlayerDamage)

        ent = self.ecsm.createEntity()
        mapLoc = self.ecsm.getEntityComponent(self.n1, LocationCartesian)
        self.ecsm.addEntityComponent(ent, LocationCartesian(mapLoc.x, mapLoc.y))
        self.ecsm.addEntityComponent(ent, Vital(100, 10))
        self.ecsm.addEntityComponent(ent, Movement(0.3, self.n0, self.n1))
        self.ecsm.addEntityComponent(ent, Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True))
        self.ecsm.addEntityComponent(ent, Faction(faction=0))

        pd.update(0, self.state, self.ecsm)

        player_vital_comp = self.ecsm.getEntityComponent(self.state.player, Vital)
        self.assertEqual(player_vital_comp.health, 100)

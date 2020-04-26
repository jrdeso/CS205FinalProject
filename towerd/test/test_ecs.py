import unittest

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
from ..Map import Map, PathType


class TestECS(unittest.TestCase):
    def setUp(self):
        self.map = Map()
        self.n1 = self.map.addNode(PathType.PATH_START, 0.15, 0.2)
        self.n2 = self.map.addNode(PathType.PATH_END, 0.9, 0.2)
        self.n3 = self.map.addNode(PathType.TOWER, 0.2, 0.1)
        self.map.addEdge(self.n1, self.n2)

        state = GameState()
        state.wave = 0
        state.map = self.map

        # Initial ECS setup
        self.maxEntities = 5
        ecsm = ECSManager(self.maxEntities)
        ecsm.registerComponent(LocationCartesian)
        ecsm.registerComponent(MapNode)
        ecsm.registerComponent(Movement)
        ecsm.registerComponent(Vital)
        ecsm.registerComponent(Attack)
        ecsm.registerComponent(Faction)
        ecsm.registerComponent(Coin)

        ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)
        ecsm.registerSystem(SpawnSystem)
        ecsm.registerSystem(PlayerDamage, Faction, LocationCartesian, Vital)

        player = ecsm.createEntity()
        ecsm.addEntityComponent(player, Vital(100, 0))
        ecsm.addEntityComponent(player, Coin(100))
        ecsm.addEntityComponent(player, Faction(1))
        state.player = player

        # Make mobs
        self.orig_coords = [(0.15, 0.2), (0.2, 0.2)]
        for i in range(len(self.orig_coords)):
            ent = ecsm.createEntity()
            ecsm.addEntityComponent(ent, LocationCartesian(*self.orig_coords[i]))
            ecsm.addEntityComponent(ent, Vital(100, 10))
            ecsm.addEntityComponent(ent, Movement(0.3, self.n1.id, self.n2.id))
            ecsm.addEntityComponent(ent, Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True))
            ecsm.addEntityComponent(ent, Faction(faction=0))

            state.entities[ent.ID] = ent
            setattr(self, f'e{i}', ent)

        # Make tower
        tower_node = self.n3
        tower_ent = ecsm.createEntity()
        # ecsm.addEntityComponent(tower_ent, LocationNode(tower_node.id))
        ecsm.addEntityComponent(tower_ent, LocationCartesian(tower_node.x, tower_node.y))
        ecsm.addEntityComponent(tower_ent, Attack(attackRange=0.5, attackSpeed=2, dmg=5, target=None, attackable=False))
        ecsm.addEntityComponent(tower_ent, Faction(faction=1))

        state.entities[tower_ent.ID] = tower_ent

        # build tree
        state.dynamicTree.add(EntityPoint2D(*self.orig_coords[0], entity=state.entities[1]))
        state.staticTree.add(EntityPoint2D(tower_node.x, tower_node.y, entity=tower_ent))

        self.state = state
        self.ecsm = ecsm

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

    def test_spawn(self):
        ss = self.ecsm.getSystem(SpawnSystem)

        self.state.wave = 1
        ss.update(0, self.state, self.ecsm)
        self.state.waveInProgress = True

        self.assertEqual(self.ecsm.em.nActive, 5)

        for i in range(4, self.maxEntities):
            locComp = self.ecsm.getEntityComponent(self.state.entities[i], LocationCartesian)
            moveComp = self.ecsm.getEntityComponent(self.state.entities[i], Movement)
            self.assertEqual(self.n1.x, locComp.x)
            self.assertEqual(self.n1.y, locComp.y)
            self.assertEqual(self.n1.id, moveComp.fromNode)
            self.assertEqual(self.n2.id, moveComp.destNode)

    def test_damage(self):
        pd = self.ecsm.getSystem(PlayerDamage)

        ent = self.ecsm.createEntity()
        self.ecsm.addEntityComponent(ent, LocationCartesian(self.n2.x, self.n2.y))
        self.ecsm.addEntityComponent(ent, Vital(100, 10))
        self.ecsm.addEntityComponent(ent, Movement(0.3, self.n1.id, self.n2.id))
        self.ecsm.addEntityComponent(ent, Attack(attackRange=0.01, attackSpeed=2, dmg=5, target=None, attackable=True))
        self.ecsm.addEntityComponent(ent, Faction(faction=0))

        pd.update(0, self.state, self.ecsm)

        player_vital_comp = self.ecsm.getEntityComponent(self.state.player, Vital)
        self.assertEqual(player_vital_comp.health, 90)

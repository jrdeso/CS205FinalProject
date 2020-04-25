import enum
import json
import kdtree
import os
import pygame
import pygame.locals

from towerd.ECS import ECSManager
from towerd.Map import Map, PathType
from towerd.component.Coin import Coin
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.LocationNode import LocationNode
from towerd.component.Movement import Movement
from towerd.component.Vital import Vital
from towerd.component.Attack import Attack
from towerd.component.Faction import Faction
from towerd.system.MovementSystem import MovementSystem
from towerd.system.AttackSystem import AttackSystem
from towerd.util.EntityPoint2D import EntityPoint2D

from towerd.Resources import Resources

R_PATHS = Resources(
    os.path.join(os.environ["DATA_DIR"], "resources.json"), mapFromDir=True
)
MAX_ENTITIES = 128


def processJson(filepath):
    with open(filepath) as f:
        jsonString = "".join([line.strip() for line in f.readlines()])
    return json.loads(jsonString)


class GameEvent(enum.IntEnum):
    START = enum.auto()
    QUIT = enum.auto()


class GameEntityType(enum.IntEnum):
    ARCHER_TOWER = enum.auto()
    MAGE_TOWER = enum.auto()
    SOLDIER_TOWER = enum.auto()
    ORC = enum.auto()


class GameState:
    def __init__(self):
        self.player = None

        self.entities = {}
        self.dynamicTree = kdtree.create(dimensions=2)
        self.staticTree = kdtree.create(dimensions=2)

        self.map = None

        self.wave = 0
        self.waveInProgress = False


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.running = False
        self.ecsm = ECSManager(MAX_ENTITIES)
        self.state = None

        self.createWindow()

    def createWindow(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        # self.background = pygame.image.load(os.path.join("xxxxxxx", "xxxxx.png"))
        # self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # pygame.mixer.music.load("xxx.mp3")
        # pygame.mixer.music.play(loops=-1)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # TODO: Get the node id mapped to with a clickable region.
                # Change None to node id.
                if event.key == pygame.locals.K_q:
                    pos = pygame.mouse.get_pos()
                    Game.createTower(
                        self.ecsm, self.state, GameEntityType.ARCHER_TOWER, None
                    )
                if event.key == pygame.locals.K_w:
                    pos = pygame.mouse.get_pos()
                    Game.createTower(
                        self.ecsm, self.state, GameEntityType.MAGE_TOWER, None
                    )
                if event.key == pygame.locals.K_e:
                    pos = pygame.mouse.get_pos()
                    Game.createTower(
                        self.ecsm, self.state, GameEntityType.SOLDIER_TOWER, None
                    )

    @staticmethod
    def createTower(ecsm, state, entityType, nodeID):
        try:
            ent = ecsm.createEntity()
        except IndexError:
            return None
        node = state.map.nodes[nodeID]

        attrPath = None
        if entityType == GameEntityType.ARCHER_TOWER:
            attrPath = R_PATHS.tower.archer_tower
        elif entityType == GameEntityType.MAGE_TOWER:
            attrPath = R_PATHS.tower.mage_tower
        elif entityType == GameEntityType.SOLDIER_TOWER:
            attrPath = R_PATHS.tower.soldier_tower
        attr = processJson(attrPath)

        ecsm.addEntityComponent(ent, LocationCartesian(node.x, node.y))
        ecsm.addEntityComponent(
            ent,
            Attack(
                attackRange=attr['attack_range'],
                attackSpeed=attr['attack_speed'],
                dmg=attr['damage'],
                target=None,
                attackable=False,
            ),
        )
        ecsm.addEntityComponent(ent, Faction(1))
        state.staticTree.add(EntityPoint2D(node.x, node.y, entity=ent))
        state.entities[ent.ID] = ent

        return ent

    @staticmethod
    def createMob(ecsm, state, entityType, x, y):
        try:
            ent = ecsm.createEntity()
        except IndexError:
            return None

        attrPath = None
        if entityType == GameEntityType.ORC:
            attrPath = R_PATHS.mob.orc
        attr = processJson(attrPath)

        ecsm.addEntityComponent(ent, LocationCartesian(x, y))
        ecsm.addEntityComponent(
            ent,
            Attack(
                attackRange=attr['attack_range'],
                attackSpeed=attr['attack_speed'],
                dmg=attr['damage'],
                target=None,
                attackable=True,
            ),
        )
        ecsm.addEntityComponent(ent, Vital(attr['health'], 0))
        ecsm.addEntityComponent(ent, Faction(0))
        state.dynamicTree.add(EntityPoint2D(x, y, entity=ent))
        state.entities[ent.ID] = ent

        return ent

    def addPlayer(self, health=100, default_coins=100):
        player_id = len(self.state.player)

        player = self.ecsm.createEntity()
        self.ecsm.addEntityComponent(player, Vital(health, 0))
        self.ecsm.addEntityComponent(player, Coin(default_coins))
        self.ecsm.addEntityComponent(player, Faction(player_id))

        self.state.player[player_id] = player

    def setupGameState(self, jsonMap):
        self.state = GameState()
        self.state.map = Map(map_json=jsonMap)
        self.state.dynamic_tree = kdtree.create(dimensions=2)
        self.state.static_tree = kdtree.create(dimensions=2)

    def setupECS(self):
        self.ecsm.registerComponent(Coin)
        self.ecsm.registerComponent(LocationCartesian)
        self.ecsm.registerComponent(LocationNode)
        self.ecsm.registerComponent(Movement)
        self.ecsm.registerComponent(Vital)
        self.ecsm.registerComponent(Attack)
        self.ecsm.registerComponent(Faction)

        self.ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        self.ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)

    def run(self, mapPath):
        self.running = True

        # self.setupAssets()
        mapJson = processJson(mapPath)

        self.setupGameState(mapJson)
        self.setupECS()

        movementSystem = self.ecsm.getSystem(MovementSystem)
        attackSystem = self.ecsm.getSystem(AttackSystem)

        dt = 0
        clock = pygame.time.Clock()
        while self.run:
            self.handleInput()

            movementSystem.update(dt, self.state, self.ecsm)
            attackSystem.update(dt, self.state, self.ecsm)

            self.draw()
            dt = clock.tick(60)

    def draw(self):
        pass

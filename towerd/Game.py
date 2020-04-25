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

MAX_ENTITIES = 128


class GameState:
    def __init__(self):
        self.player = None

        self.entities = {}
        self.dynamicTree = kdtree.create(dimensions=2)
        self.staticTree = kdtree.create(dimensions=2)

        self.map = None

        self.wave = 0
        self.waveInProgress = False


class GameEntityType(enum.IntEnum):
    ArcherTower = enum.auto()
    MageTower = enum.auto()
    SoldierTower = enum.auto()
    Orc = enum.auto()


class Game:
    def __init__(self, width, height, datadir):
        self.width = width
        self.height = height

        resourcePath = os.path.join(datadir, 'resources.json')
        self.R = Resources(resourcePath, mapFromDir=True)

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
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.locals.K_q:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        self.createEntity(pos[0], pos[1], GameEntityType.ArcherTower)
                if event.key == pygame.locals.K_w:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        self.createEntity(pos[0], pos[1], GameEntityType.MageTower)
                if event.key == pygame.locals.K_e:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        self.createEntity(pos[0], pos[1], GameEntityType.SoldierTower)
                else:
                    return False

    def createEntity(self, x, y, entityType):
        """
        Create entity at the location. Usually should only be used for towers
        or debugging mobs.
        """
        def process_json(filepath):
            with open(self.R.tower.archer_tower) as f:
                jsonLines = f.readlines()
                jsonArr = [line.strip for line in jsonLines]
                jsonString = ''.join(jsonArr)
            return jsonString

        if entityType == GameEntityType.ArcherTower:
            obj = json.loads(process_json(self.R.tower.archer_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.5, attackSpeed = 2, dmg = 7, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))
        elif entityType == GameEntityType.Orc:
            obj = json.loads(process_json(self.R.mob.orc))
            ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.01, attackSpeed = 1, dmg = 10, target = None, attackable = True))
            self.ecsm.addEntityComponent(ent, Vital(100, 10))
            self.ecsm.addEntityComponent(ent, Faction(faction=0))
        elif entityType == GameEntityType.MageTower:
            obj = json.loads(process_json(self.R.tower.mage_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.3, attackSpeed = 1, dmg = 10, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))
        elif entityType == GameEntityType.SoldierTower:
            obj = json.loads(process_json(self.R.tower.soldier_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.01, attackSpeed = 1, dmg = 4, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))

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
        self.ecsm = ECSManager(5)
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
        with open(mapPath) as f:
            mapJson = json.loads("".join([line.strip() for line in f.readlines()]))

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

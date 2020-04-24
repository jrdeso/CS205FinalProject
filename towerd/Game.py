import dataclasses
import enum
import json
import kdtree
import os
import pygame

from ECS import ECSManager
from Map import Map, PathType
from component.LocationCartesian import LocationCartesian
from component.LocationNode import LocationNode
from component.Movement import Movement
from component.Vital import Vital
from component.Attack import Attack
from component.Faction import Faction
from system.MovementSystem import MovementSystem
from system.AttackSystem import AttackSystem
from util.EntityPoint2D import EntityPoint2D

from Resources import Resources
_R = Resources('../data/resources.json', gatherFromDir=True)

MAX_ENTITIES = 128


@dataclasses.dataclass
class GameState:
    entities: dict = {}
    dynamicTree: object = None
    staticTree: object = None

    map: Map = None

    wave: int = 0
    waveInProgress: bool = False


class GameEntityType(enum.IntEnum):
    ArcherTower = enum.auto()
    Orc = enum.auto()


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 700

        self.run = False
        self.ecsm = ECSManager(MAX_ENTITIES)
        self.state = None

        self.createWindow()

    def createWindow(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load(os.path.join("xxxxxxx", "xxxxx.png"))
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        pygame.mixer.music.load("xxx.mp3")
        pygame.mixer.music.play(loops=-1)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_Q:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        # create archer tower
                        pass
                if event.key == pygame.K_W:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        # create mage tower
                        pass
                if event.key == pygame.K_E:
                    pos = pygame.mouse.get_pos()
                    if pos:
                        # create melee tower
                        pass
                else:
                    pass

    def createEntity(self, x, y, entityType):
        """
        Create entity at the location. Usually should only be used for towers
        or debugging mobs.
        """
        def process_json(filepath):
            with open(_R.tower.archer_tower) as f:
                jsonLines = f.readlines()
                jsonArr = [line.strip for line in jsonLines]
                jsonString = ''.join(jsonArr)
            return jsonString

        if entityType == GameEntityType.ArcherTower:
            obj = json.loads(process_json(_R.tower.archer_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.5, attackSpeed = 2, dmg = 7, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))
        elif entityType == GameEntityType.Orc:
            obj = json.loads(process_json(_R.mob.orc))
            ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.01, attackSpeed = 1, dmg = 10, target = None, attackable = True))
            self.ecsm.addEntityComponent(ent, Vital(100, 10))
            self.ecsm.addEntityComponent(ent, Faction(faction=0))
        elif entityType == GameEntityType.MageTower:
            obj = json.loads(process_json(_R.tower.mage_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.3, attackSpeed = 1, dmg = 10, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))
        elif entityType == GameEntityType.SoldierTower:
            obj = json.loads(process_json(_R.tower.soldier_tower))
            tower_ent = self.ecsm.createEntity()
            self.ecsm.addEntityComponent(tower_ent, LocationCartesian(x, y))
            self.ecsm.addEntityComponent(tower_ent, Attack(attackRange = 0.01, attackSpeed = 1, dmg = 4, target = None, attackable = False))
            self.ecsm.addEntityComponent(tower_ent, Faction(faction = 1))


    def setupGameState(self, jsonMap):
        self.state = GameState()
        self.state.map = Map(map_json=jsonMap)
        self.state.dynamic_tree = kdtree.create(dimensions=2)
        self.state.static_tree = kdtree.create(dimensions=2)

    def setupECS(self):
        self.ecsm = ECSManager(5)
        self.ecsm.registerComponent(LocationCartesian)
        self.ecsm.registerComponent(LocationNode)
        self.ecsm.registerComponent(Movement)
        self.ecsm.registerComponent(Vital)
        self.ecsm.registerComponent(Attack)
        self.ecsm.registerComponent(Faction)

        self.ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        self.ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)

    def run(self, mapPath):
        self.run = True

        self.setupAssets()
        self.setupGameState()
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

    def draw():
        pass

import enum
import json
import kdtree
import os
import pygame
import pygame.locals

from towerd.ECS import ECSManager
from towerd.component.Coin import Coin
from towerd.component.LocationCartesian import LocationCartesian
from towerd.component.MapNode import MapNode, PathType
from towerd.component.Movement import Movement
from towerd.component.Vital import Vital
from towerd.component.Attack import Attack
from towerd.component.Faction import Faction
from towerd.component.Sprite import Sprite
from towerd.system.MovementSystem import MovementSystem
from towerd.system.AttackSystem import AttackSystem
from towerd.system.SpriteSystem import SpriteSystem
from towerd.system.SpawnSystem import SpawnSystem
from towerd.system.PlayerDamage import PlayerDamage
from towerd.system.RemoveDeadEntitiesSystem import RemoveDeadEntitiesSystem

from towerd.ui.UIFactory import UIFactory, UIType

from towerd.util.EntityPoint2D import EntityPoint2D

from towerd.Resources import Resources

A_PATHS = Resources(
    os.path.join(os.environ["ASSET_DIR"], "resources.json"), mapFromDir=True
)
R_PATHS = Resources(
    os.path.join(os.environ["DATA_DIR"], "resources.json"), mapFromDir=True
)
MAX_ENTITIES = 1024


def processJson(filepath):
    with open(filepath) as f:
        jsonString = "".join([line.strip() for line in f.readlines()])
    return json.loads(jsonString)


class GameEvent(enum.IntEnum):
    START = enum.auto()
    QUIT = enum.auto()
    NEXT_WAVE = enum.auto()
    CREATE_TOWER = enum.auto()


class GameEntityType(enum.IntEnum):
    ARCHER_TOWER = enum.auto()
    MAGE_TOWER = enum.auto()
    SOLDIER_TOWER = enum.auto()
    ORC = enum.auto()


class GameState:
    def __init__(self):
        self.player = None
        self.playerVital = None

        self.entities = {}
        self.dynamicTree = kdtree.create(dimensions=2)
        self.staticTree = kdtree.create(dimensions=2)
        self.mapTree = kdtree.create(dimensions=2)

        self.mapEntities = {}

        self.wave = 0
        self.waveInProgress = False
        self.gameover = False


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.running = True
        self.playing = False
        self.ecsm = ECSManager(MAX_ENTITIES)
        self.state = None

        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        self.curInterface = None

        self.changeInterface(UIType.MAIN_MENU)

    def changeInterface(self, uiType):
        self.curInterface = UIFactory.createUI(uiType, self.win.get_size())

        if self.curInterface.music:
            pygame.mixer.music.load(self.curInterface.music)
            pygame.mixer.music.play(loops=-1)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def createTower(ecsm, state, entityType, x, y):
        try:
            ent = ecsm.createEntity()
        except IndexError:
            return None

        attrPath = None
        if entityType == GameEntityType.ARCHER_TOWER:
            attrPath = R_PATHS.tower.archer
        elif entityType == GameEntityType.MAGE_TOWER:
            attrPath = R_PATHS.tower.mage
        elif entityType == GameEntityType.SOLDIER_TOWER:
            attrPath = R_PATHS.tower.soldier
        attr = processJson(attrPath)

        node, _ = state.mapTree.search_nn((x, y))
        ep2d = node.data

        def calcDist(x0, y0, x1, y1):
            import math
            return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

        dist = calcDist(*ep2d.coords, x, y)
        print(dist, *ep2d.coords, x, y)
        if dist > 5:
            return None

        ecsm.addEntityComponent(ent, LocationCartesian(*ep2d.coords))
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
        ecsm.addEntityComponent(ent, Sprite(A_PATHS.tower.archer))
        state.staticTree.add(EntityPoint2D(*ep2d.coords, entity=ent))
        state.entities[ent.ID] = ent

        print('created', ent)

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
        ecsm.addEntityComponent(ent, Sprite(A_PATHS.mob.orc))
        ecsm.addEntityComponent(ent, Movement(attr['movement_speed'], None, None))
        state.dynamicTree.add(EntityPoint2D(x, y, entity=ent))
        state.entities[ent.ID] = ent

        return ent

    def buildMap(self, mapObj):
        ents = [self.ecsm.createEntity() for i in range(len(mapObj))]

        for ent, key in zip(ents, mapObj):
            pathType, coords, edges = mapObj[key].values()
            pathType = PathType.GetEnum(pathType)
            edges = [ents[int(e)] for e in edges]
            self.ecsm.addEntityComponent(ent, LocationCartesian(*coords))
            self.ecsm.addEntityComponent(ent, MapNode(pathType, edges))
            if pathType == PathType.PATH_START:
                self.ecsm.addEntityComponent(ent, Sprite(A_PATHS.path.start))
            elif pathType == pathType.PATH_END:
                self.ecsm.addEntityComponent(ent, Sprite(A_PATHS.path.end))
            elif pathType == pathType.TOWER:
                self.ecsm.addEntityComponent(ent, Sprite(A_PATHS.tower.tower))
                self.state.mapTree.add(EntityPoint2D(*coords, entity=ent))
            self.state.mapEntities[ent.ID] = ent

    def addPlayer(self, health=100, default_coins=100):
        player = self.ecsm.createEntity()
        self.ecsm.addEntityComponent(player, Vital(health, 0))
        self.ecsm.addEntityComponent(player, Coin(default_coins))
        self.ecsm.addEntityComponent(player, Faction(player.ID))

        self.state.player = player
        self.state.playerVital = self.ecsm.getEntityComponent(player, Vital)

    def setupGameState(self):
        self.state = GameState()
        self.state.dynamic_tree = kdtree.create(dimensions=2)
        self.state.static_tree = kdtree.create(dimensions=2)

    def setupECS(self):
        self.ecsm.registerComponent(Coin)
        self.ecsm.registerComponent(LocationCartesian)
        self.ecsm.registerComponent(MapNode)
        self.ecsm.registerComponent(Movement)
        self.ecsm.registerComponent(Vital)
        self.ecsm.registerComponent(Attack)
        self.ecsm.registerComponent(Faction)
        self.ecsm.registerComponent(Sprite)

        self.ecsm.registerSystem(MovementSystem, LocationCartesian, Movement)
        self.ecsm.registerSystem(AttackSystem, Attack, Faction, LocationCartesian)
        self.ecsm.registerSystem(SpriteSystem, LocationCartesian, Sprite)
        self.ecsm.registerSystem(SpawnSystem, MapNode, LocationCartesian)
        self.ecsm.registerSystem(PlayerDamage, Faction, LocationCartesian, Attack, Vital)
        self.ecsm.registerSystem(RemoveDeadEntitiesSystem, Vital)

    def handleGameEvent(self, state, args):
        if state == GameEvent.START:
            self.changeInterface(UIType.IN_GAME)

            self.setupGameState()
            self.setupECS()
            self.addPlayer()

            mapJson = processJson(args)
            self.buildMap(mapJson)
            self.playing = True
        elif state == GameEvent.CREATE_TOWER:
            Game.createTower(self.ecsm, self.state, *args)
        elif state == GameEvent.NEXT_WAVE:
            self.state.wave += 1
            self.state.waveInProgress = False
        elif state == GameEvent.QUIT:
            self.playing = False
            self.changeInterface(UIType.MAIN_MENU)

    def start(self):
        """
        Handles the display of any menus or overlays.
        """

        clock = pygame.time.Clock()
        dt = 0
        while self.running:
            dt = clock.tick(60)
            stateArgsBuffer = []
            for event in pygame.event.get():
                stateArgsBuffer.append(self.curInterface.handleEvent(event))
                self.curInterface.processEvents(event)

            for state, args in stateArgsBuffer:
                self.handleGameEvent(state, args)

            self.curInterface.update(dt)
            screen = self.curInterface.draw(self.state)

            if self.playing:
                movementSystem = self.ecsm.getSystem(MovementSystem)
                attackSystem = self.ecsm.getSystem(AttackSystem)
                spawnSystem = self.ecsm.getSystem(SpawnSystem)
                spriteSystem = self.ecsm.getSystem(SpriteSystem)
                playerDamageSystem = self.ecsm.getSystem(PlayerDamage)
                removeDeadEntitiesSystem = self.ecsm.getSystem(RemoveDeadEntitiesSystem)

                if not self.state.waveInProgress:
                    spawnSystem.addWave(self.state.wave)
                    self.state.waveInProgress = True

                spawnSystem.update(dt, self.state, self.ecsm)
                movementSystem.update(dt, self.state, self.ecsm)
                attackSystem.update(dt, self.state, self.ecsm)
                spriteSystem.update(dt, self.state, self.ecsm)
                playerDamageSystem.update(dt, self.state, self.ecsm)
                removeDeadEntitiesSystem.update(dt, self.state, self.ecsm)
                spriteSystem.drawSprites(screen)

                playerVital = self.ecsm.getEntityComponent(self.state.player, Vital)
                if playerVital.health <= 0:
                    self.playing = False
                    self.state.gameover = True

            self.win.blit(screen, (0, 0))

            pygame.display.update()

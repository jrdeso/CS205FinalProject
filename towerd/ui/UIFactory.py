import enum

from towerd.ui.MainMenu import MainMenu
from towerd.ui.GameUI import GameUI


class UIType(enum.IntEnum):
    MAIN_MENU = enum.auto()
    IN_GAME = enum.auto()


class UIFactory:
    def createUI(uiType, resolution):
        if uiType == UIType.MAIN_MENU:
            return MainMenu(resolution)
        elif uiType == UIType.IN_GAME:
            return GameUI(resolution)

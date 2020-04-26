import enum

from towerd.ui.MainMenu import MainMenu


class UIType(enum.IntEnum):
    MAIN_MENU = enum.auto()
    IN_GAME = enum.auto()


class UIFactory:
    def createUI(uiType, resolution):
        if uiType == UIType.MAIN_MENU:
            return MainMenu(resolution)

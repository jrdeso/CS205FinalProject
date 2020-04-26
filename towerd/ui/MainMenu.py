import pygame
import pygame_gui

from towerd.ui.UI import UI


class MainMenu(pygame.Surface, UI):
    def __init__(self, *args, **kwargs):
        pygame.Surface.__init__(self, *args, **kwargs)
        UI.__init__(self, self.get_size())

        self.font = pygame.font.Font("freesansbold.ttf", 72)
        self.bgColor = pygame.Color((100, 100, 100))
        self.fgColor = pygame.Color((255, 255, 255))

        width, height = self.get_size()
        self.startButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Start",
            manager=self.manager,
        )
        self.quitButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width - 100, 0), (100, 50)),
            text="Quit",
            manager=self.manager,
        )

        welcomeMessage = self.font.render(
            "Tower Defense", True, self.fgColor
        )

        self.windowItems = [
            (welcomeMessage, (int(width / 6), int(height / 2))),
        ]

    def draw(self, state):
        self.fill(self.bgColor)
        for item, args in self.windowItems:
            self.blit(item, args)
        self.manager.draw_ui(self)
        return self

    def handleEvent(self, event):
        from towerd.Game import GameEvent, R_PATHS
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.startButton:
                    return (GameEvent.START, R_PATHS.map.default)
                if event.ui_element == self.quitButton:
                    exit(0)
        return None, None

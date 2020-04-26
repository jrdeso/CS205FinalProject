import pygame
import pygame_gui

from towerd.ui.UI import UI


class MainMenu(UI):
    def __init__(self, resolution):
        super().__init__(resolution)
        background = pygame.Surface(resolution)
        background.fill(pygame.Color((100, 100, 100)))

        font = pygame.font.Font("freesansbold.ttf", 72)
        welcomeMessage = font.render(
            "Tower Defense", True, (252, 252, 252)
        )

        # make button to start game - quit
        self.startButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 0), (100, 50)),
            text="Start",
            manager=self.manager,
        )
        self.blits = [
            (background, (0, 0)),
            (welcomeMessage, (int(resolution[0] / 5), int(resolution[1] / 4))),
        ]

    def handleEvent(self, event):
        from towerd.Game import GameEvent, R_PATHS
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.startButton:
                    return (GameEvent.START, R_PATHS.map.default)

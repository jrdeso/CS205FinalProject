import pygame
import pygame_gui

from towerd.ui.UI import UI


class GameUI(UI):
    def __init__(self, resolution):
        super().__init__(resolution)
        background = pygame.Surface(resolution)
        background.fill(pygame.Color((100, 100, 100)))

        font = pygame.font.Font("freesansbold.ttf", 72)
        # welcomeMessage = font.render(
        #     "Tower Defense", True, (252, 252, 252)
        # )

        # button to spawn new wave
        self.nextWave = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Next Wave",
            manager=self.manager,
        )

        # Button to quit game - can remain (used to exit during game)
        self.quitButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((700, 0), (100, 50)),
            text="Quit",
            manager=self.manager,
        )

        self.blits = [
            (background, (0, 0)),  # Got rid of welcome message from this UI
        ]

    def handleEvent(self, event):
        from towerd.Game import GameEvent, R_PATHS
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.quitButton:
                    exit(0)
                if event.ui_element == self.nextWave:
                    # TODO: Call new wave through game
                    pass
            return None, None

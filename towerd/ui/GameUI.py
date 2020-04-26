import pygame
import pygame_gui

from towerd.ui.UI import UI


class GameUI(pygame.Surface, UI):
    def __init__(self, *args, **kwargs):
        pygame.Surface.__init__(self, *args, **kwargs)
        UI.__init__(self, self.get_size())

        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.bgColor = pygame.Color((100, 100, 100))
        self.fgColor = pygame.Color((255, 255, 255))

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

    def handleEvent(self, event):
        from towerd.Game import GameEvent, GameEntityType
        width, height = self.get_size()
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = pos[0]/width * 100, pos[1]/height * 100
            if keys[pygame.K_q]:
                return GameEvent.CREATE_TOWER, (GameEntityType.ARCHER_TOWER, *pos)
            if keys[pygame.K_w]:
                return GameEvent.CREATE_TOWER, (GameEntityType.MAGE_TOWER, *pos)
            if keys[pygame.K_e]:
                return GameEvent.CREATE_TOWER, (GameEntityType.SOLDIER_TOWER, *pos)
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.quitButton:
                    return GameEvent.QUIT, None
                if event.ui_element == self.nextWave:
                    return GameEvent.NEXT_WAVE, None
        return None, None

    def draw(self, state):
        self.fill(self.bgColor)
        healthText = self.font.render(
            f"Player 1: {state.playerVital}", True, self.fgColor
        )
        waveText = self.font.render(
            f"Wave: {state.wave}", True, self.fgColor
        )
        gameoverText = self.font.render(
            f"GAME OVER", True, self.fgColor
        )
        width, height = self.get_size()
        if state.gameover:
            self.blit(gameoverText, (width/2, height/2))
        self.blit(healthText, (10, height - 50))
        self.blit(waveText, (10, height - 25))
        self.manager.draw_ui(self)
        return self

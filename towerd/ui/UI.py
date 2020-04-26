import abc
import pygame
import pygame_gui

from towerd.Game import GameEvent


class UI(abc.ABC):
    def __init__(self, resolution, surface, background):
        self.manager = pygame_gui.UIManager(resolution)

        self.processEvents = self.manager.process_events
        self.update = self.manager.update
        self.drawUI = self.manager.draw_ui

        font = pygame.font.Font('freesansbold.ttf', 72)
        welcomeMessage = font.render("Tower Defense", True, (252, 252, 252))  # color - white

        # make button to start game - quit
        startButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Start',
                                                   manager=self.manager)
        clock = pygame.time.Clock()
        # bool variable holds if user has begun game or not -
        startScreen = True
        while startScreen:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == startButton:
                            GameEvent(1)  # sets game event to start
                            startScreen = False
                            #TODO: Move to game from here

                self.manager.process_events(event)
            self.manager.update(time_delta)
            surface.blit(background, (0, 0))
            surface.blit(welcomeMessage, (int(resolution[0] / 5), int(resolution[1] / 4)))  # current hardcoded coordin
            self.manager.draw_ui(surface)

            pygame.display.update()


    def handleEvents(self, event):
        """
        Handle user inputs that are associated with the UI elements in this
        object.

        :param event: pygame.event.Event
        :return: tuple of (GameEvent, data)
        """
        raise NotImplementedError

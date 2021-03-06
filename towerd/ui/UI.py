import abc
import pygame_gui


class UI(abc.ABC):
    def __init__(self, resolution):
        self.manager = pygame_gui.UIManager(resolution)

        self.windowItems = []
        self.music = None

        self.processEvents = self.manager.process_events
        self.update = self.manager.update
        self.drawUI = self.manager.draw_ui

    def handleEvent(self, event):
        """
        Handle user inputs that are associated with the UI elements in this
        object.

        :param event: pygame.event.Event
        :return: tuple of (GameEvent, data)
        """
        raise NotImplementedError

    def draw(self, state):
        raise NotImplementedError

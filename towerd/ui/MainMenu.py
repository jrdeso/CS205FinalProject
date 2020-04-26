import pygame
import pygame_gui

from towerd.ui.UI import UI


class MainMenu(UI):
    def __init__(self, resolution):
        # init pygame
        pygame.init()
        pygame.display.set_caption("Tower Defense")

        surface = pygame.display.set_mode(resolution)
        background = pygame.Surface(resolution)
        background.fill(pygame.Color((100, 100, 100)))


        super().__init__(resolution, surface, background)

        #while True:
        #    pygame.display.update()


    def handleEvents(self, event):
        # TODO: handle events associated with a ui element
        pass


m = MainMenu((800, 600))

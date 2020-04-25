import pygame
import pygame_gui

from towerd.ui.UI import UI


class MainMenu(UI):
    def __init__(self, resolution):
        # init pygame
        pygame.init()
        pygame.display.set_caption("Tower Defense")
        font = pygame.font.Font('freesansbold.ttf', 72)
        surface = pygame.display.set_mode(resolution)
        background = pygame.Surface(resolution)
        background.fill(pygame.Color((192, 192, 192)))

        WELCOME = font.render("Tower Defense", True, (252, 252, 252))  # color - white

        surface.blit(WELCOME, (int(resolution[0] / 5), int(resolution[1] / 4)))  # current hardcoded coordinates

        super().__init__(resolution)

        #while True:
        #    pygame.display.update()


    def handleEvents(self, event):
        # TODO: handle events associated with a ui element
        pass


m = MainMenu((800, 600))

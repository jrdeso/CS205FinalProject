import os
import pygame
import time
import random


pygame.mixer.music.load("xxx.mp3") #To play music while the game is running (still have to decided the track that we are going to play)

class ECSManager:

    def __init__(self):
    	self.width = 1350
    	self.height = 700
    	self.bg = pygame.image.load(os.path.join("FLA", "xxx.png")) #I was not able to find a decent free background for the game


    def update(self, dt, state):
        time.sleep(random.random()) #update all systems


    def handle_input():
    	x, y = pygame.mouse.get_pos()
    	name_list = ["buy_archer", "buy_mage", "buy_soldier"]
    	object_list = []


    def draw():
        time.sleep(random.random())

        self.blit(self.bg, (0, 0))

        for tw in self.towers:
        	tw.draw()

        for enm in self.enemies:
        	tw.draw()






#Game Logic

quit = False
quit_time = time.time() + 10


dt = 0
ecsm = ECSManager()


#create state below(maybe better as a class)
state = {} #track entities, kdtree, etc
state['entities'] = []
state['map'] = None #Create map here


while not quit:
    start = time.time()
    #use ECSManager to handle user input (create towers, etc)
    handle_input()
    #do updates, iterate over systems
    ecsm.update(dt, state)
    #do drawing, draw the entities/map/etc
    draw()

    stop = time.time()
    dt = stop - start  #this would be the clock.tick
    print('fps', 1/dt)


    #handle quit
    if time.time() > quit_time:
    	quit = True



    



import pygame

class Mob:

	sprites = []

    def __init__(self, x, y):
        self.x = x #This represents the coordinates x of the mob
        self.y = y #This represents the coordinates y of the mob
        self.animation_count = 0 #This variable is used to animate the mobs (We could do them without animating them). It starts at 0 which is the default position for going straight
        self.health = 100 #Base health for basic mobs is 100. We have to adjust this number
        self.sprite =  None


    def draw(self, win): #This method will draw the emobs
    	win.blit() #Fill this with apropiate information


   	def move(self): #This method control the movements of the mobs
   		self.animation_count = self.animation_count + 1
   		if self.animation_count >= len(self.sprites):
   			self.animation_count = 0 #This resets the animations back


   	def killed(self, dmg): #Method for when an enemy is killed by a tower
   		self.health = self.health - dmg
   		if self.health <= 0:
   			return True
   		return False


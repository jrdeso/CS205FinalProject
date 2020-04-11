import pygame

class Mob:

	#sprites = []

    def __init__(self, x, y):
        self.x = x #This represents the coordinates x of the mob
        self.y = y #This represents the coordinates y of the mob
        self.animation_count = 0 #This variable is used to animate the mobs (We could do them without animating them). It starts at 0 which is the default position for going straight
        self.health = 100 #Base health for basic mobs is 100. We have to adjust this number
        self.alive = True
        #self.sprite =  None

	''' Old code, I don't want to delete it but I think this will be moved to Game class eventually
	
    def draw(self, win): #This method will draw the emobs
    	win.blit() #Fill this with apropiate information
	

   	def move(self): #This method control the movements of the mobs
   		self.animation_count = self.animation_count + 1
   		if self.animation_count >= len(self.sprites):
   			self.animation_count = 0 #This resets the animations back
	'''

	# Not sure how Game will tell Mob to move, but it should be something like this
	def move(self, newX, newY):
		self.x = newX
		self.y = newY

	def takeDamage(self, damage):
		self.health -= damage
		if(self.health <= 0):
			# Mob is dead, return true to Game
			self.alive = False
			return True
		return False
import os
import pygame
import time



#music for the game (still have to decide which audio we are gonna use)
pygame.mixer.music.load("xxx.mp3")

class Game:
	def __init__(self):
		self.width = 1200 #Width of the pygame window
		self.height = 700 #Height of the pygame window
		self.win = pygame.display.set_mode((self.width, self.height))
		self.mobs = []
		self.towers = []
		self.player_lives = 20
		self.player_money = 1000
		self.background = pygame.image.load(os.path.join("xxxxxxx", "xxxxx.png"))
		self.background = pygame.transform.scale(self.background, (self.width, self.height))
		self.wave = 0 #The starter wave
		self.current_wave = waves[self.wave][:]
		self.timer = time.time()


	def build_tower():

		x, y = pygame.mouse.get_pos()
		name_list = ["archer", "mage", "soldier"]
		#self.win.blit() ###With this we draw the towers in the pygame window


	def generate_wave(self):

		if sum(self.current_wave) == 0:
			if len(self.mobs) == 0:
				self.wave += 1
				self.current_wave = waves[self.wave]
		else:
			wave_enemies = [Mobs()]

            for x in range(len(self.current_wave)):
				if self.current_wave[x] != 0:
					self.enemys.append(wave_enemies[x])
					self.current_wave[x] = self.current_wave[x] - 1
					break

    def gen_enemies(self): #This method handles all the waves generation

		if(self.current_wave = 0):
			if(len(self.enemies)) == 0:
				self.wave += 1 #We add a new wave
				self.current_wave = waves[self.wave]



	def run(self): #This is the run method to control all the dynamics of the game
		pygame.mixer.music.play(loops = -1)#The music will play undefinitely because the loop = -1
		run = True
		clock = pygame.time.Clock() #To set the FPS of the game
		while run:
			clock.tick(60) #This runs the fame at 60 FPS	


			# main event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_Q:
						pos = pygame.mouse.get_pos()
						if pos == :#i do not know how to check if the coords are valid for placing a tower
							#draw archer tower
					if event.key == pygame.K_W:
						pos = pygame.mouse.get_pos()
						if pos == :#same as before
							#draw mage tower
					if event.key == pygame.K_E:
						pos = pygame.mouse.get_pos()
						if pos == :#same as before
							#draw melee tower

					else:
						


			#in case the player loses
			if self.lives <= 0:
				run = False








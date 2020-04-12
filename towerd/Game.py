import os
import pygame

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



	def run(self): #This is the run method to control all the dynamics of the game
		run = True
		clock = pygame.time.Clock() #To set the FPS of the game
		while run:
			clock.tick(60) #This runs the fame at 60 FPS


			# main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
			pygame.display.update()


	#def draw(self):
	#	self.win.blit(self.background, (0, 0))
	#	pygame.display.update()


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
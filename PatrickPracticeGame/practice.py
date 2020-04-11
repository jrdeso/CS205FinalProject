import os, sys, pygame
import map
import mob
import tower


def buildChooser(tilesMap,xCoord, yCoord, towers):
	#yesTile = pygame.image.load("yes.jpg")
	#noTile = pygame.image.load("no.jpg")
	chosen = False
	font = pygame.font.Font(pygame.font.get_default_font(), 32) 
	black = 0, 0, 0
	text = font.render('Build Tower (y/n)?', True, black)
	textRect = text.get_rect()  
	while chosen == False:
		for event in pygame.event.get():
			screen.blit(text, textRect) 
			#print("HERE")
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_y: 
					tilesMap.buildTower(xCoord, yCoord)
					#print("Built Tower")
					towers.append(tower.Tower(xCoord, yCoord))
					return True
				elif event.key == pygame.K_n:
					return False
		pygame.display.flip()


pygame.init()

size = width, height = 800, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

greenTile = pygame.image.load("green.jpg")
brownTile = pygame.image.load("brown.jpg")
yellowTile = pygame.image.load("yellow.jpg")
redTile = pygame.image.load("red.jpg")
mobTile = pygame.image.load("mob.jpg")

tilesMap = map.Map()

firstMob = mob.Mob()

towers = []

paused = False

#dead = False

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	if(paused == False):
		screen.fill(black)
		
		for x in range(8):
			for y in range(8):
				#print("Drawing tiles")
				if(tilesMap.map[x][y] == 0):
					screen.blit(greenTile, (x*100, y*100))
				elif(tilesMap.map[x][y] == 1):
					screen.blit(brownTile, (x*100, y*100))
				elif(tilesMap.map[x][y] == 2):
					#print("in red")
					screen.blit(redTile, (x*100, y*100))
				elif(tilesMap.map[x][y] == 3):
					print("Making mob tile")
					screen.blit(mobTile, (x*100, y*100))

		pos = pygame.mouse.get_pos()

		tilePos = (int(pos[0]/100), int(pos[1]/100))

		#print(tilePos)
		screen.blit(yellowTile, (tilePos[0]*100, tilePos[1]*100))
		if(pygame.mouse.get_pressed()[0]):
			#print("CLICKED")
			#screen.blit(yesTile, (300,300))
			#screen.blit(noTile, (300, 600))
			paused = True
			buildChooser(tilesMap, tilePos[0], tilePos[1], towers)
			paused = False

		# Create a mob 
		if(firstMob.alive == True):
			print("if firstMob alive")
			tilesMap.moveMob(firstMob.xCoord, firstMob.yCoord)

			# Find next tile on the path
			nextTile = tilesMap.getNextPathTile(firstMob.xCoord, firstMob.yCoord) 

			# Move the mob
			#print("Time = ", pygame.time.get_ticks())
			#print("Time % 100 = ", (int(pygame.time.get_ticks() / 100)) % 10)
			if(int(pygame.time.get_ticks() / 100) % 10 == 0):
				if(nextTile[0] != -1):
					firstMob.move(nextTile[0], nextTile[1])

		if(int(pygame.time.get_ticks() / 100) % 10 == 0):
			# Check if any tower has a mob in range and deal damage if so
			for theTower in towers:
				minXCoord = theTower.xCoord - theTower.range
				maxXCoord = theTower.xCoord + theTower.range
				minYCoord = theTower.yCoord - theTower.range
				maxYCoord = theTower.yCoord + theTower.range
				for x in range(minXCoord, maxXCoord):
					for y in range(minYCoord, maxYCoord):
						if(firstMob.xCoord == x and firstMob.yCoord == y):
							dead = firstMob.takeDamage(theTower.damage)
							if(dead):
								print("HERE")
								tilesMap.mobKilled(firstMob.xCoord, firstMob.yCoord)


		pygame.display.flip()

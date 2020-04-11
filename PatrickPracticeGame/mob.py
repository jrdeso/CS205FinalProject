class Mob:
	def __init__(self):
		self.health = 30
		self.xCoord = 0
		self.yCoord = 2
		self.alive = True

	def move(self, newX, newY):
		self.xCoord = newX
		self.yCoord = newY

	def takeDamage(self, damage):
		print("In takeDamage")
		self.health -= damage
		if(self.health <= 0):
			print("Mob has died")
			self.alive = False
			return True
		return False
		
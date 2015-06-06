import random

class Ball:
	
	xCoords = 10/2
	yCoords = 10/2
	xBearing = random.choice([-1,1])
	yBearing = random.choice([-1,1])
	
	def __init__(self, speed, size):
		self.speed = speed
		self.size = size
		self.coords = {'x':self.xCoords, 'y':self.yCoords}
		
	class Pig:
		pigx = Ball.xCoords
		def __init__(self,speed):
			self.speed = speed
			
x = Ball(10,10)
pig = Ball.Pig(10)

print pig.pigx
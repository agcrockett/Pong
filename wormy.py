# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#		       R	G	 B
WHITE		= (255,	255, 255)
BLACK		= (0,	0,	 0)
RED			= (255, 0,	 0)
GREEN		= (0,	255, 0)
DARKGREEN 	= (0,	155, 0)
DARKGRAY	= (40,	40,	 40)
BGCOLOR		= BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freensansbold.ttf', 18)
	pygame.display.set_caption('Wormy')
	
	showStartScreen()
	while True:
		runGame()
		showGameOverScreen()

		
def runGame():
	# Set a random start point
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	wormCoords = [{'x': startx,	'y':starty},
			{'x': startx - 1, 'y':starty},
			{'x': startx - 2, 'y': starty}]
	direction = RIGHT
	
	# Start the apple in a random place.
	apple = getRandomLocation()

while True:
	for event in pygame.event.get(): # event handling loop
		if event.type == QUIT:
			terminate()
		elif event.type == KEYDOWN:
			if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
				direction = LEFT
			elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
				direction = RIGHT
			elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
				direction = UP
			elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
				direction = DOWN
			elif event.key == K_escape:
				terminate()
		# check if the worm has hit itself or the edge
		if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x']==CELLWIDTH or wormCoords[HEAD]
['y'] == -1 or wormCoords[HEAD]['y']==CELLHEIGHT:
			return # game over
		for wormBody in wormCoords[1:]:
			if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
				return # game over
		
		# check if the worm has eaten an apply
		if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
			# don't remove worm's tail segment
			apple = getRandomLocation()
		else:
			del wormCoords[-1]
		
		# move the worm by adding a segment in the direction it is moving
		if direction == UP:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
		wormCoords.insert(0, newHead)
		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(len(wormCoords) - 3)
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	
def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
	
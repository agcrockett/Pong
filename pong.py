import random, pygame, sys
from pygame.locals import *
import pygame.gfxdraw

# CONSTANTS

FPS = 60
BOARDSPEED = 20
BALLSPEED = 5

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

BLOCKSIZE = 20

BOARDLENGTH = BLOCKSIZE * 4
BOARDHEIGHT = BLOCKSIZE

assert WINDOWWIDTH % BLOCKSIZE == 0, "Window width must be a multiple of block size."
assert WINDOWHEIGHT % BLOCKSIZE == 0, "Window height must be a multiple of block size."

BLOCKWIDTH = int(WINDOWWIDTH / BLOCKSIZE)
BLOCKHEIGHT = int(WINDOWHEIGHT / BLOCKSIZE)

userScore = 0
opponentScore = 0

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

#---------------------------------------------------------------------------------------------

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, ballDirX, ballDirY
	pygame.init()
	pygame.key.set_repeat(20, 20)
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Pong')
		
	DISPLAYSURF.fill(BGCOLOR)
	
	
	while True:
		ballDirX = random.choice([-1,0,1]) # -1 = left, 1 = right
		ballDirY = random.choice([-1,1]) # -1 = up, 1 = down
		runGame()
	
	
def setCoords():
	global userBoardCoords
	global opponentBoardCoords
	global ballCoords
		
	ballStartx = WINDOWWIDTH/2
	ballStarty = WINDOWHEIGHT/2
	
	userStartx = WINDOWWIDTH/2 - BOARDLENGTH/2
	userStarty = WINDOWHEIGHT - BLOCKSIZE
	
	opponentStartx = WINDOWWIDTH/2-BOARDLENGTH/2
	opponentStarty = 0
	
	userBoardCoords = {'x':userStartx, 'y':userStarty}
	opponentBoardCoords = {'x':opponentStartx, 'y':opponentStarty}
	ballCoords = {'x':ballStartx, 'y':ballStarty}
	
	
def checkEvents():
	for event in pygame.event.get(): # event handling loop
		if event.type == QUIT:
			quit()	
		elif event.type == KEYDOWN:
			if (event.key == K_LEFT or event.key == K_a) and not userBoardRect.colliderect(leftBorderRect):
				userBoardCoords['x'] -= BOARDSPEED
					
			elif (event.key == K_RIGHT or event.key == K_d) and not userBoardRect.colliderect(rightBorderRect):
				userBoardCoords['x'] += BOARDSPEED
						
			elif event.key == K_ESCAPE:
				quit()
		
	
def updateDisplay():
	DISPLAYSURF.fill(BGCOLOR)
	drawBorders()
	drawUserBoard(userBoardCoords)
	drawOpponentBoard(opponentBoardCoords)	
	drawBall(ballCoords)
	moveBall(ballCoords)
	moveOpponent()
	drawGrid()
	drawScore(userScore, opponentScore)
	pygame.display.update()

	
def runGame():
	
	setCoords()
	
	while True: # main game loop
		checkEvents()
		updateDisplay()
		
		ballCollided = ballCollisions()
		
		if ballCollided == True:
			return
		else:
			pass
		
		FPSCLOCK.tick(FPS)

		
def ballCollisions():
	global ballDirX, ballDirY
	global opponentScore
	global userScore
	
	# Collide with top board
	if ballRect.colliderect(opponentBoardRect):
		print "collision"
		ballDirY = 1 # Go down
		
	# Collide with bottom board	
	elif ballRect.colliderect(userBoardRect):
		print "collision"
		ballDirY = -1 # Go up
	
	# Collide with left border	
	elif ballRect.colliderect(leftBorderRect):
		print "collision"
		ballDirX = 1 # Go right

	# Collide with right border	
	elif ballRect.colliderect(rightBorderRect):
		print "collision"
		ballDirX = -1 # Go left
		
	# Update score
	if ballCoords['y'] <= -1:
		userScore += 1
		return True # round over - Player wins
		
	elif ballCoords['y'] >= WINDOWHEIGHT+20:
		opponentScore += 1
		return True # round over - Opponent wins
	else:
		return False
	
	
def terminate():
    pygame.quit()
    sys.exit()

	
def drawUserBoard(userBoardCoords):
	global userBoardRect
	
	x = userBoardCoords['x']
	y = userBoardCoords['y']
	
	userBoardRect = pygame.Rect(x, y, BOARDLENGTH, BOARDHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, userBoardRect)
	
	
def drawOpponentBoard(opponentBoardCoords):
	global opponentBoardRect
	
	x = opponentBoardCoords['x']
	y = opponentBoardCoords['y']
	opponentBoardRect = pygame.Rect(x, y, BOARDLENGTH, BOARDHEIGHT)
	pygame.draw.rect(DISPLAYSURF, WHITE, opponentBoardRect)
	
	
def drawGrid():
    for x in range(0, WINDOWWIDTH, BLOCKSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, BLOCKSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
	
	
def moveBall(ballCoords):
	ballCoords['x'] += ballDirX * BALLSPEED
	ballCoords['y'] += ballDirY * BALLSPEED
	return ballCoords
	
	
def moveOpponent():
	global opponentBoardCoords
	
	# Ball moving left
	if ballDirX == -1 and not opponentBoardRect.colliderect(leftBorderRect):
		if opponentBoardCoords['x'] > ballCoords['x']:
			opponentBoardCoords['x'] -= BOARDSPEED
			
	# Ball moving right
	elif ballDirX == 1 and not opponentBoardRect.colliderect(rightBorderRect):
		if opponentBoardCoords['x'] < ballCoords['x']:
			opponentBoardCoords['x'] += BOARDSPEED
	
	print "Ballx", ballCoords['x']
	print "Bally", ballCoords['y']
	
	
	
def drawBall(ballCoords):
	global ballRect
	
	x = ballCoords['x']
	y = ballCoords['y']
	
	ball = pygame.draw.circle(DISPLAYSURF, WHITE, (x,y), 5)
	ballRect = pygame.Rect(ball)
	
	
def drawBorders():
	global leftBorderRect
	global rightBorderRect
	
	leftx = 0
	lefty = 0
	
	rightx = WINDOWWIDTH-BLOCKSIZE
	righty = 0
	
	leftBorderRect = pygame.Rect(leftx, lefty, BLOCKSIZE, WINDOWHEIGHT)
	pygame.draw.rect(DISPLAYSURF, GREEN, leftBorderRect)
	
	rightBorderRect = pygame.Rect(rightx, righty, BLOCKSIZE, WINDOWHEIGHT)
	pygame.draw.rect(DISPLAYSURF, GREEN, rightBorderRect)
	
	#pygame.draw.line(DISPLAYSURF, GREEN, (0, WINDOWHEIGHT/2), (WINDOWWIDTH,WINDOWHEIGHT/2), 10)
	
	
def drawScore(userScore, opponentScore):
	playerScoreSurf = BASICFONT.render('%s' % (userScore), True, WHITE)
	playerScoreRect = playerScoreSurf.get_rect()
	playerScoreRect.topleft = (WINDOWWIDTH - 55, WINDOWHEIGHT/2+BLOCKSIZE)
	DISPLAYSURF.blit(playerScoreSurf, playerScoreRect)
	
	opponentScoreSurf = BASICFONT.render('%s' % (opponentScore), True, WHITE)
	opponentScoreRect = opponentScoreSurf.get_rect()
	opponentScoreRect.topleft = (WINDOWWIDTH - 55, WINDOWHEIGHT/2-BLOCKSIZE*2)
	DISPLAYSURF.blit(opponentScoreSurf, opponentScoreRect)
	
	
if __name__ == '__main__':
	main()

    
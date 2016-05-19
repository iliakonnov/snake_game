# -*- coding: utf-8 -*-
import time
import pygame
import sys
from pygame.locals import *
from TorWorld import *
from snake import *

pygame.init()
argv = sys.argv
if len(argv) == 3 + 1:  # Использовать файл мира
	world_type = 1
	snakelength = int(argv[1])
	SpdOfGame = int(argv[2])
	world = TorWorld(argv[3])
	FoodMany = None
	BricksMany = None
elif len(argv) == 6 + 1:  # Использовать файл мира
	world_type = 0
	snakelength = int(argv[1])
	SpdOfGame = int(argv[2])
	widhtWorld = int(argv[3])
	heigthWorld = int(argv[4])
	FoodMany = int(argv[5])
	BricksMany = int(argv[6])
	ABIW = widhtWorld * heigthWorld - ((widhtWorld - 1) + (heigthWorld - 1)) * 2  # all_blocks_in_world
	NBIW = FoodMany + BricksMany  # need_blocks_in_world
	if ABIW < NBIW:
		raise ValueError("Use other size of world or number of food and bricks")
	world = TorWorld(widhtWorld, heigthWorld)
else:
	snakelength = int(raw_input("Enter how long snake (1-10)> "))
	if snakelength < 1:
			raise ValueError("Use other snake length!")

	SpdOfGame = int(raw_input("Enter how fast game (20-25)> "))
	world_type = raw_input("Enter filename of world (leave empty for random)> ")
	if len(world_type) != 0:
		FoodMany = None
		BricksMany = None
		world = TorWorld(world_type)
	else:
		widhtWorld = int(raw_input("Enter widht of world (50-80)> "))
		heigthWorld = int(raw_input("Enter heigth of world (50-70)> "))
		FoodMany = int(raw_input("Enter how many food (5-10)> "))
		BricksMany = int(raw_input("Enter how many bricks (1-5)> "))

		ABIW = widhtWorld * heigthWorld - ((widhtWorld - 1) + (heigthWorld - 1)) * 2  # all_blocks_in_world
		NBIW = FoodMany + BricksMany  # need_blocks_in_world
		if ABIW < NBIW:
			raise ValueError("Use other size of world or number of food and bricks")
		world = TorWorld(widhtWorld, heigthWorld)

cellSize = 12
screen_width = world.width * cellSize
screen_height = world.height * cellSize
screen = pygame.display.set_mode([screen_width, screen_height])
left, right, up, down = False, False, False, False
turbo = False


def ShowWorld(world, screen, scale, images):
	for coords, ID in world.GetDiff().iteritems():
		x, y = coords
		idPicture = ID
		if idPicture is None:
			idPicture = 0
		a = x * scale
		b = y * scale
		screen.blit(images[idPicture], (a, b))
	pygame.display.flip()

imageSize = cellSize - 2
images = [pygame.Surface((imageSize, imageSize)) for i in range(5)]
imagesColors = [(255, 255, 255),  # 1
				(78, 135, 96),    # 2
				(140, 86, 88),    # 3
				(116, 89, 75),    # 4
				(0, 163, 232)]    # 5
for i in range(len(images)):
	images[i].fill(imagesColors[i])

screen.fill((255, 255, 255))
snake = Snake(world, 2, 1, 3, 4, world.height, world.width)
startSnake = [[i, 0] for i in xrange(snakelength)]

snake.Init(startSnake, (0, 1))
if not world_type == 1:
	snake.FoodAndBricks(FoodMany, BricksMany)
timer = pygame.time.Clock()
ShowWorld(snake.world, screen, cellSize, images)

work = True
print "Start"
startTime = time.time()
while work:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_LEFT:
			if not right:
				left, right, up, down = True, False, False, False
				snake.TurnLeft()

		if event.type == KEYDOWN and event.key == K_RIGHT:
			if not left:
				left, right, up, down = False, True, False, False
				snake.TurnRight()

		if event.type == KEYDOWN and event.key == K_UP:
			if not down:
				left, right, up, down = False, False, True, False
				snake.TurnUp()

		if event.type == KEYDOWN and event.key == K_DOWN:
			if not up:
				left, right, up, down = False, False, False, True
				snake.TurnDown()

		if event.type == KEYDOWN and event.key == K_SPACE:
			if turbo:
				SpdOfGame = SpdOfGame / 2
			else:
				SpdOfGame = SpdOfGame * 2
			turbo = not turbo

		if event.type == QUIT:
			pygame.quit()
			work = False

	if not snake.Move():
			print("GAME OVER")
			pygame.quit()
			work = False
	else:
		if work:
			ShowWorld(snake.world, screen, cellSize, images)
			timer.tick(SpdOfGame)
score = snake.score
levels = (score / FoodMany) + 1
print('Eated: {}'.format(score))
print('Time: {} seconds'.format(round(time.time() - startTime), 1))
print('Levels: {}'.format(levels))
print('Bricks: {}'.format(BricksMany * levels))
print('Length: {}'.format(snakelength + score))
raw_input('Press enter to exit.')

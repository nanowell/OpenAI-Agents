# Python game from 4th dimension


import pygame
import sys
from pygame.locals import *
import random
import time

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Shooting Game')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up the player and food data structure
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 20
player = pygame.Rect(300, 100, 50, 50)
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, 640 - FOODSIZE), random.randint(0, 480 - FOODSIZE), FOODSIZE, FOODSIZE))

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6


# run the game loop
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, 480 - player.height)
                player.left = random.randint(0, 640 - player.width)

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        # add new food
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, 640 - FOODSIZE), random.randint(0, 480 - FOODSIZE), FOODSIZE, FOODSIZE))
    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # move the player
    if moveDown and player.bottom < 480:
        player.top += MOVESPEED
    if moveUp and player.top > 0:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < 640:
        player.right += MOVESPEED

    # draw the block onto the surface
    pygame.draw.rect(windowSurface, WHITE, player)

    # create score
    font = pygame.font.Font(None, 48)
    score = len(foods)
    text = font.render(str(score), 1, WHITE)
    windowSurface.blit(text, (500, 0))

    #create exit
    font = pygame.font.Font(None, 24)
    text = font.render('Press ESC to quit', 1, WHITE)
    windowSurface.blit(text, (0, 0))
    
    #create restart
    font = pygame.font.Font(None, 24)
    text = font.render('Press R to restart', 1, WHITE)
    windowSurface.blit(text, (0, 24))
    
    # check if the player has intersected with any food squares.
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)

    # draw the food
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface, GREEN, foods[i])

    #draw glow around the food
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface, RED, foods[i], 5)

    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)

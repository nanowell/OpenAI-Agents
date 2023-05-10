import random
import time
import copy
import logging
import numpy as np
import pygame

WIDTH = 60
HEIGHT = 40

pygame.init()
screen = pygame.display.set_mode((WIDTH * 10, HEIGHT * 10))

# Create a 2D NumPy array for the cells
nextCells = np.random.choice(['#', ' '], size=(WIDTH, HEIGHT), p=[0.5, 0.5])

while True:
    try:
        print('\n\n\n\n\n')
        currentCells = copy.deepcopy(nextCells)

        # Draw the current state of the game on the window
        def draw_game_state(screen, currentCells):
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    if currentCells[x, y] == '#':
                        pygame.draw.rect(screen, (255, 255, 255), (x * 10, y * 10, 10, 10))

        draw_game_state(screen, currentCells)

        # Create a surface for the next frame
        next_frame = pygame.Surface((WIDTH * 10, HEIGHT * 10))
        next_frame.fill((0, 0, 0))

        # Calculate the next step's cells based on current step's cells using NumPy
        nextCells = np.copy(currentCells)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                # Get neighboring coordinates using modulo operator
                leftCoord, rightCoord = (x - 1) % WIDTH, (x + 1) % WIDTH
                aboveCoord, belowCoord = (y - 1) % HEIGHT, (y + 1) % HEIGHT

                # Count number of living neighbors using NumPy
                numNeighbors = np.sum(currentCells[leftCoord:rightCoord + 1, aboveCoord:belowCoord + 1] == '#') - int(currentCells[x, y] == '#')

                # Set cell based on Conway's Game of Life rules using NumPy
                if currentCells[x, y] == '#':
                    nextCells[x, y] = '#' if numNeighbors in {2, 3} else ' '
                else:
                    nextCells[x, y] = '#' if numNeighbors == 3 else ' '

        # Blend the current frame with the next frame
        current_frame = pygame.transform.scale(screen, (WIDTH * 10, HEIGHT * 10))
        
        # Set the alpha value for the next frame
        next_frame.set_alpha(128)  # 128 is an example value; you can adjust it for the desired blending effect
        
        # Blit the next frame onto the current frame
        current_frame.blit(next_frame, (0, 0))
        
        # Display the blended frame
        screen.blit(current_frame, (0, 0))
        pygame.display.flip()


        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program...")
        break
    except Exception as e:
        logging.error(e)
        print("An error occurred. Please check the log file.")
        quit()

import numpy as np
import time

WIDTH = 60
HEIGHT = 20

# Create a random array of 0s and 1s for the cells:
nextCells = np.random.randint(0, 2, size=(WIDTH, HEIGHT))

while True: # Main program loop.
    print('\n\n\n\n\n') # Separate each step with newlines.
    currentCells = nextCells.copy()

    # Print currentCells on the screen:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print('#' if currentCells[x][y] == 1 else ' ', end='') # Print the # or space.
        print() # Print a newline at the end of the row.

    # Calculate the next step's cells based on current step's cells:
    
    # Create an array that stores the number of living neighbors for each cell:
    neighbors = np.zeros((WIDTH, HEIGHT), dtype=int)
    
    # Shift the array in eight directions and add them up:
    for dx, dy in [(-1,-1), (-1,0), (-1,+1), (0,-1), (0,+1), (+1,-1), (+1,0), (+1,+1)]:
        neighbors += np.roll(np.roll(currentCells, dx, axis=0), dy, axis=1)
    
    # Apply the rules of the game using np.where:
    nextCells = np.where(currentCells == 1,
                         np.where((neighbors == 2) | (neighbors == 3), 1 , 0),
                         np.where(neighbors == 3 , 1 , 0))
    
    time.sleep(0.1) # Add a 1-second pause to reduce flickering.

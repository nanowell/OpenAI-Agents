# Python and P5.js


from _typeshed import HasFileno
import math
import random
from typing import runtime_checkable

from pyp5js import *

# sketch's global variables

# the number of balls
n = 10

# the balls' positions
x = []
y = []

# the balls' velocities
vx = []
vy = []

# the balls' colors
colors = []

# the balls' sizes
sizes = []
width, height = 600, 600

def noLoop():
    """
    Stops the animation loop.
    """

    global loop

    loop = False

    print("noLoop")



def createCanvas():
    """
    Creates a P5.js canvas.
    """
    global canvas, sketch
    
    canvas = document.createElement('canvas')
    canvas.setAttribute('width', '600')
    canvas.setAttribute('height', '600')
    sketch = document.getElementById('sketch')
    sketch.appendChild(canvas)
    sketch.style.display = 'block'
    noLoop()
    print("hello")

def color(r, g, b):
    """
    Returns the P5.js color format from RGB.
    """

    return f'rgba({r}, {g}, {b}, 1.0)'

def setup():
    """
    Setup function.
    """

    global x, y, vx, vy, colors, sizes

    createCanvas(600, 600)

    # create the balls' positions
    for i in range(n):
        x.append(random.randint(0, width))
        y.append(random.randint(0, height))

    # create the balls' velocities
    for i in range(n):
        vx.append(random.randint(-2, 2))
        vy.append(random.randint(-2, 2))

    # create the balls' colors
    for i in range(n):
        colors.append(color(random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255)))

    # create the balls' sizes
    for i in range(n):
        sizes.append(random.randint(10, 50))

def image(img, x, y):
    """
    Displays an image at a given position.
    """

    global canvas, sketch

    # get the context
    ctx = canvas.getContext('2d')

    # draw the image
    ctx.drawImage(img, x, y)

def createGraphics():
    """
    Creates a P5.js canvas.
    """
    global canvas, sketch
    window = html.window
    document = window.document
    canvas = document.createElement('canvas')
    canvas.setAttribute('width', '600')
    canvas.setAttribute('height', '600')
    sketch = document.getElementById('sketch')
    sketch.appendChild(canvas)
    sketch.style.display = 'block'
    noLoop()
    

def ellipse(x, y, w, h, c):
    """
    Draws an ellipse at a given position with a given size and color.
    """

    global canvas, sketch

    # get the context
    ctx = canvas.getContext('2d')

    # set the color
    ctx.fillStyle = c

    # draw the ellipse
    ctx.beginPath()
    ctx.ellipse(x, y, w / 2, h / 2, 0, 0, 2 * math.pi)
    ctx.fill()

def background(r, g, b):
    """
    Sets the background color.
    """

    background = createGraphics(width, height)
    background.beginDraw()
    background.background(r, g, b)
    background.endDraw()
    image(background, 0, 0)

def draw():
    """
    Draw function.
    """

    global x, y, vx, vy, colors, sizes

    background(255)

    # move the balls
    for i in range(n):
        x[i] += vx[i]
        y[i] += vy[i]

        # check if the balls hit the walls
        if x[i] > width or x[i] < 0:
            vx[i] = -vx[i]
        if y[i] > height or y[i] < 0:
            vy[i] = -vy[i]

        # draw the balls
        ellipse(x[i], y[i], sizes[i], sizes[i], colors[i])


# start the sketch
if __name__ == '__main__':
    createGraphics()
    runtime_checkable()
# Desktop screen grab


from os import times
import cv2
import numpy as np
from PIL import ImageGrab
import time

def screen_grab(x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    return ImageGrab.grab(box)

# q to quit
def main():
    last_time = time.time()
    while True:
        # 800x600 windowed mode
        printscreen =  np.array(screen_grab(0,40,800,640))
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()

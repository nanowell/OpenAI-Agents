import cv2
import numpy as np

# Define the range of red color in HSV
lower_red = np.array([150, 150, 50])
upper_red = np.array([180, 255, 150])

cap = cv2.VideoCapture(0)

# Use the fastest setting for capture
cap.set(cv2.CAP_PROP_FPS, 120)

while True:
    _, frame = cap.read()

    # Convert the frame from BGR (Blue-Green-Red) to HSV (Hue-Saturation-Value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask by thresholding the image to only select red pixels
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Show the original frame and the result of applying the red mask
    cv2.imshow('frame', frame)
    cv2.imshow('res', red_res)

    # Exit if the user presses the Esc key
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

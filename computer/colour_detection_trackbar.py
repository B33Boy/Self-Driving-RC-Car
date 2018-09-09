import cv2
import numpy as np

# Different programs have different range for HSV
# OpenCV HSV range is H: 0-179, S: 0-255, V: 0-255

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

#Trackbars
cv2.namedWindow("Trackbars")


cv2.createTrackbar("Lower - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Lower - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Upper - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper - V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()

    #hsv min is [0, 0, 0]
    #hsv max is [180, 255, 255]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Connect trackbar to manipulate values
    l_h = cv2.getTrackbarPos("Lower - H", "Trackbars")
    l_s = cv2.getTrackbarPos("Lower - S", "Trackbars")
    l_v = cv2.getTrackbarPos("Lower - V", "Trackbars")
    u_h = cv2.getTrackbarPos("Upper - H", "Trackbars")
    u_s = cv2.getTrackbarPos("Upper - S", "Trackbars")
    u_v = cv2.getTrackbarPos("Upper - V", "Trackbars")

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow("Frame", frame)
    #cv2.imshow("Mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)

    if key == 27:
        break
    elif key == ord('a'):
        print(l_h, l_s, l_v, u_h, u_s, u_v)

cap.release()
cv2.destroyAllWindows()


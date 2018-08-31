import numpy as np
import cv2

e1 = cv2.getTickCount()

x = 10**10
y = 4**1
x = x/y

e2 = cv2.getTickCount()
time = (e2-e1)/cv2.getTickFrequency()


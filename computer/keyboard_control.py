import serial
import pygame
from pygame.locals import *


class TeleopTest():

    def __init__(self):
        #initialize pygame and create small window where our keypresses will be detected
        pygame.init()
        pygame.display.set_mode((100, 100))

        #Include port and baudrate, with timeout of 1 second
        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        self.connected = True
        self.moveCar()


    def moveCar(self):
        while self.connected:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.ser.write(chr(3).encode())

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        self.ser.write(chr(4).encode())

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.ser.write(chr(5).encode())

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.ser.write(chr(6).encode())

                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        self.ser.write(chr(1).encode())

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.ser.write(chr(2).encode())

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.ser.write(chr(0).encode())
                        self.ser.close()
                        self.connected = False

                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(chr(0).encode())


if __name__ == "__main__":
    TeleopTest()

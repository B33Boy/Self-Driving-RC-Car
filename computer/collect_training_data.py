import socket
import serial
import numpy as np
import cv2
import os
import pygame
from pygame.locals import *
import time


class CollectTrainingData(object):

    def __init__(self, host, port, serial_port, image_size):

        # initialize, bind, listen, and accept data from socket
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(0)
        self.conn, self.client_addr = self.sock.accept()
        self.conn = self.conn.makefile('rb')

        # initialize serial port
        # send_frames is for loop control
        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.send_frames = True

        # used for reshaping data
        self.image_size = image_size

        # create labels
        #   ([[1  0  0]     this means move forward left
        #     [0  1  0]     this means move forward
        #     [0  0  1]])   this means move forward right
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1

        pygame.init()
        pygame.display.set_mode((300, 300))

    def collect(self):

        # statistics
        saved_frame = 0
        total_frame = 0
        clicks_forward = 0
        clicks_forward_left = 0
        clicks_forward_right = 0

        # start measuring time
        start = cv2.getTickCount()

        # Our inputs and expected outputs
        # the x is the unrolled image, and the y is the keypress
        X = np.empty((1, self.image_size))
        y = np.empty((1, 3))
        #print(X, y)

        try:

            stream_bytes = b' '
            frame = 1

            while self.send_frames:

                stream_bytes += self.conn.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    cv2.imshow('image', image)

                    height, width = image.shape
                    roi = image[int(height/2):height, :]

                    temp_array = roi.reshape(1, int(height/2) * width).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    for event in pygame.event.get():

                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                                print("Forward Right")
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[2]))
                                saved_frame += 1
                                clicks_forward_right += 1
                                self.ser.write(chr(5).encode())

                            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                                print("Forward Left")
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[0]))
                                saved_frame += 1
                                clicks_forward_left += 1
                                self.ser.write(chr(6).encode())

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                                print("Reverse Right")
                                self.ser.write(chr(7).encode())

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                                print("Reverse Left")
                                self.ser.write(chr(8).encode())

                            # simple orders
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[1]))
                                saved_frame += 1
                                clicks_forward += 1
                                self.ser.write(chr(1).encode())

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                self.ser.write(chr(2).encode())

                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                #X = np.vstack((X, temp_array))
                                #y = np.vstack((y, self.k[4]))
                                saved_frame += 1
                                #clicks_forward += 1
                                self.ser.write(chr(3).encode())

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                #X = np.vstack((X, temp_array))
                                #y = np.vstack((y, self.k[0]))
                                saved_frame += 1
                                #clicks_forward += 1
                                self.ser.write(chr(4).encode())

                            # exit
                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print("Exit")
                                self.send_frames = False
                                self.ser.write(chr(0).encode())
                                self.ser.close()
                                break

                        elif event.type == pygame.KEYUP:
                            self.ser.write(chr(0).encode())

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            file_name = str(int(time.time()))
            directory = "training_data"

            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print("X shape: ", X.shape)
            print("y shape: ", y.shape)

            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Clicks forward: ", clicks_forward)
            print("Clicks forward_right: ", clicks_forward_right)
            print("Clicks forward_left: ", clicks_forward_left)

        finally:
            self.conn.close()
            self.sock.close()


if __name__ == '__main__':

    host, port, serial_port = "192.168.0.15", 50002, "/dev/ttyUSB0"

    #Size of one frame (cut in half because we only care for the lower half)
    image_size = 120*320

    collectData = CollectTrainingData(host, port, serial_port, image_size)
    collectData.collect()





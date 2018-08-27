import SocketServer
import threading
import numpy as np
import cv2
import sys


ultrasonic_data = None

# BaseRequestHandler is used to process incoming requests
class UltrasonicHandler(SocketServer.BaseRequestHandler):

    data = " "

    def handle(self):

        while self.data:
            self.data = self.request.recv(1024)
            ultrasonic_data = float(self.data.split('.')[0])
            print(ultrasonic_data)


# VideoStreamHandler uses streams which are file-like objects for communication
class VideoStreamHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        pass


class SelfDriverServer(object):

    def __init__(self, host, portUS, portCam):
        self.host = host
        self.portUS = portUS
        self.portCam = portCam

    def startUltrasonicServer(self):
        # Create the Ultrasonic server, binding to localhost on port 50001
        server = SocketServer.TCPServer((self.host, self.portUS), UltrasonicHandler)
        server.serve_forever()

    def startVideoServer(self):
        # Create the video server, binding to localhost on port 50002
        server = SocketServer.TCPServer((self.host, self.portCam), VideoStreamHandler)
        server.serve_forever()

    def start(self):
        ultrasonic_thread = threading.Thread(target=self.startUltrasonicServer)
        ultrasonic_thread.daemon = True
        ultrasonic_thread.start()
        self.startVideoServer()


if __name__ == "__main__":

    # From SocketServer documentation
    HOST, PORTUS, PORTCAM = '192.168.0.18', 50001, 50002
    sdc = SelfDriverServer(HOST, PORTUS, PORTCAM)

    sdc.start()


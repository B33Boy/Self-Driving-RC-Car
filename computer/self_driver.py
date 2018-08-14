import SocketServer
import threading

ultrasonic_data = None

#Subclass BaseRequestHandler and override the handle method
class UltrasonicHandler(SocketServer.BaseRequestHandler):

    data = " "

    def handle(self):
        global ultrasonic_data

        while self.data:
            self.data = self.request.recv(1024)
            ultrasonic_data = float(self.data.split('.')[0])
            print(ultrasonic_data)

class VideoStreamHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        pass


class Self_Driver_Server:

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

    #From SocketServer documentation
    HOST, PORTUS, PORTCAM = '192.168.0.13', 50001, 50002
    sdc = Self_Driver_Server(HOST, PORTUS, PORTCAM)

    sdc.start()


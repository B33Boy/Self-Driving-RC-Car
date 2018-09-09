import SocketServer
import threading
import numpy as np
import cv2
import sys
import serial
from keras.models import load_model
from self_driver_helper import SelfDriver

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

    # Include port and baudrate, with timeout of 1 second
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    model = load_model("saved_model/nn_model.h5")#####################################################

    def handle(self):

        stream_bytes = b''
        driver = SelfDriver(self.ser)

        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    #image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]
                    cv2.imshow('image', roi)
                    image_array = roi.flatten().astype(np.float32)
                    prediction = self.model.predict_classes(image_array)
                    print("Prediction is", prediction)
                    # get prediction and then steer
                    if(int(ultrasonic_data) < 40):
                        print("Stopping car because of obstacle.")
                        self.driver.stop()
                        ultrasonic_data = None

                    driver.steer(prediction)

        finally:
            cv2.destroyAllWindows()
            sys.exit()





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
    HOST, PORTUS, PORTCAM = '192.168.0.15', 50001, 50002
    sdc = SelfDriverServer(HOST, PORTUS, PORTCAM)

    sdc.start()


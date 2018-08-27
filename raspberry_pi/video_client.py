import socket
import io
import struct
import time
import picamera
import sys

class SplitFrames(object):

    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.frameCount = 0

    def write(self, buf):

        #ff and d8 are magic numbers to indicate the start of a jpg
        if buf.startswith(b'\xff\xd8'):

            #Get current position of stream
            size = self.stream.tell()
            if size > 0:

                #Write length of file sent and flush the write buffers
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()

                #Reset stream and send image data
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))

                #Reset stream and add to the frame frameCount
                self.stream.seek(0)
                self.frameCount += 1

        #Here we write to stream whereas previously we write to file-like object
        self.stream.write(buf)

client_socket = socket.socket()
client_socket.connect(('192.168.0.18', 50002))

#Configure to write bytes to the file-like object
connection = client_socket.makefile('wb')

try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution=(320, 240), framerate=30) as camera:

        #Wait for camera initialization
        time.sleep(2)
        start = time.time()

        #Keep camera on for 30 min
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(sys.maxint)
        camera.stop_recording()

        #write a 0 to signify the end of stream
        connection.write(struct.pack('<L', 0))

finally:
    finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (output.frameCount, finish-start, output.frameCount / (finish-start)))
    connection.close()

client_socket.close()

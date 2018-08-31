import os
import numpy as np
import cv2
import socket


class VideostreamImages(object):

    def __init__(self, host, port):

        self.sock = socket.socket()
        self.sock.bind((host, port))

        self.sock.listen(0)
        self.conn, self.addr = self.sock.accept()
        self.conn = self.conn.makefile('rb')

        self.streamVideo()

    def streamVideo(self):

        try:
            stream_bytes = b''
            #Counts number of files in
            count = len(next(os.walk("chess_board"))[2])
            print("There are currently %d images in chess_board folder" % count)

            while True:

                stream_bytes += self.conn.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('image', image)
                    k = cv2.waitKey(1)

                    # esc key to break out of loop
                    if k==27:
                        break

                    # space key to save image to chess_board folder
                    elif k == 32:
                        count += 1
                        cv2.imwrite("chess_board/Image_%d.jpg" % count, image)
                        print("Take Image %d" % count)

                    # d key to delete last image
                    elif k == 100:
                        if count > 0:
                            os.remove("chess_board/Image_%d.jpg" % count)
                            print("Removed Image #%d" % count)
                            count -= 1
                        else:
                            print("No images left to remove!")

        finally:
            self.conn.close()
            self.sock.close()





if __name__ == '__main__':

    host, port = "192.168.0.18", 50002
    VideostreamImages(host, port)

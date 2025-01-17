import math
import cv2


class SelfDriver(object):

    def __init__(self, ser):
        self.ser = ser

    def steer(self, prediction):

        if prediction == [1.0, 0.0, 0.0]:
            self.ser.write(chr(6).encode())
        elif prediction == [0.0, 1.0, 0.0]:
            self.ser.write(chr(1).encode())

        elif prediction == [0.0, 0.0, 1.0]:
            self.ser.write(chr(5).encode())
        else:
            self.stop()

    def stop(self):
        self.ser.write(chr(0).encode())


class DistanceToCamera(object):

    def __init__(self):
        # camera params
        self.alpha = 8.0 * math.pi / 180    # degree measured manually
        self.v0 = 119.865631204             # from camera matrix
        self.ay = 332.262498472             # from camera matrix

    def calculate(self, v, h, x_shift, image):
        # compute and return the distance from the target point to the camera
        d = h / math.tan(self.alpha + math.atan((v - self.v0) / self.ay))
        if d > 0:
            cv2.putText(image, "%.1fcm" % d,
                        (image.shape[1] - x_shift, image.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return d

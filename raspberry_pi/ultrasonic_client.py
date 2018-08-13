import RPi.GPIO as GPIO
import time
import socket


class UltrasonicClient:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        self.TRIG = 16
        self.ECHO = 18

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.0.13', 8002))

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)

    def getDistance(self):
        GPIO.output(self.TRIG, False)
        time.sleep(2)
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)

        return distance


    def cleanup(self):
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        #Create object u, while True, call the distance function, print it,
        # and send the data through the socket. Sleep for half a second.
        u = UltrasonicClient()
        while True:
            dist = u.getDistance()
            print("Distance is %.1f cm" %dist)
            u.sock.send(str(dist))
            time.sleep(0.5)
    except KeyboardInterrupt:
        u.sock.close()
        u.cleanup()

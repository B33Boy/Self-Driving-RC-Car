import RPi.GPIO as GPIO
import time


class UltrasonicClient:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        self.TRIG = 16
        self.ECHO = 18

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

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
        u = UltrasonicClient()
        while True:
            u.getDistance()
    except KeyboardInterrupt:
        u.cleanup()

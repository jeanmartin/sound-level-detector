from threading import Thread
from settings import Settings
import RPi.GPIO as GPIO
import time, logging

class DistanceMeasurer:
    def __init__(self):
        logging.basicConfig(format=Settings.LOG_FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(Settings.LOG_LEVEL)

        self.trig_pin = 19
        self.echo_pin = 13

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def start(self):
        self.thread = Thread(target=self.worker)
        self.thread.deamon = True
        self.thread.start()

    def worker(self):
        self.logger.info('Starting worker')
        while True:
            self.settle()
            distance = self.measure_distance()
            distance = round(distance, 2)
            self.logger.info('Measured {0}cm'.format(distance))

    def measure_distance(self):
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        while GPIO.input(self.echo_pin)==0:
            start = time.time()
        while GPIO.input(self.echo_pin)==1:
            end = time.time()

        duration = end - start
        return duration * 17150

    def settle(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(1)

# Should we cleanup?
# GPIO.cleanup()

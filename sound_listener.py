from queue import Queue
from threading import Thread
import alsaaudio, time, audioop, logging
from led_controller import LEDController
from settings import Settings

class SoundListener:
    CARD = 'front:CARD=GoMic,DEV=0'

    def __init__(self, threshold, buffer_size, event_queue):
        logging.basicConfig(format=Settings.LOG_FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.event_queue = event_queue

        self.threshold = threshold
        self.buffer_size = buffer_size
        self.buffer = [0] * self.buffer_size

        self.mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, self.CARD)
        self.mic.setchannels(1)
        self.mic.setrate(8000)
        self.mic.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.mic.setperiodsize(160)

        self.sound_on = False

        self.led_controller = LEDController()

        self.queue = Queue()
        self.start()

    def start(self):
        # Thread 1: listen for changes in input values (sent by app.py)
        self.input_thread = Thread(target=self.input_worker)
        self.input_thread.daemon = True
        self.input_thread.start()
        # Thread 2: listen to the mic and noise level
        self.mic_thread = Thread(target=self.mic_worker)
        self.mic_thread.daemon = True
        self.mic_thread.start()

    def input_worker(self):
        self.logger.info('Starting input_worker')
        while True:
            event = self.queue.get()
            self.update_setting(event[0], event[1])
            self.queue.task_done()
            time.sleep(.001)

    def update_setting(self, type, value):
        # as of now we consider the incoming values to be validated before
        if type == 'threshold':
            self.logger.info('Updating threshold to {0}'.format(value))
            self.threshold = value
        elif type == 'buffer_size':
            self.logger.info('Updating buffer_size to {0}'.format(value))
            difference = value - self.buffer_size
            if difference > 0:
                # increase
                self.buffer = ([0] * difference) + self.buffer
            else:
                # decrease
                self.buffer = self.buffer[-difference:]
            self.buffer_size = value

    def mic_worker(self):
        self.logger.info('Starting mic_worker')
        while True:
            l, data = self.mic.read()

            if l:
                try:
                    current = audioop.rms(data, 2)
                    self.buffer = self.buffer[1:]
                    self.buffer.append(current)
                    avg = sum(self.buffer) / len(self.buffer)
                    if avg > self.threshold:
                        if not self.sound_on:
                            self.logger.info('Over volume threshold')
                            self.sound_on = True
                            self.led_controller.led_on()
                            self.event_queue.put(['over_volume_threshold', { 'threshold': self.threshold, 'buffer_size': self.buffer_size }])
                    else:
                        if self.sound_on:
                            self.logger.info('Below volume threshold')
                            self.sound_on = False
                            self.led_controller.led_off()
                            self.event_queue.put(['below_volume_threshold', { 'threshold': self.threshold, 'buffer_size': self.buffer_size }])
                    time.sleep(.001)
                except audioop.error as e:
                    if "{0}".format(e) != "not a whole number of frames":
                        raise e
                    time.sleep(.001)

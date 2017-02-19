from queue import Queue
from threading import Thread
import alsaaudio, time, audioop
from led_controller import LEDController

class SoundListener:
    CARD = 'front:CARD=GoMic,DEV=0'

    def __init__(self, threshold, noise_level_buffer_size, event_queue):
        self.event_queue = event_queue

        self.threshold = threshold
        self.noise_level_buffer_size = noise_level_buffer_size
        self.noise_level_buffer = [0] * self.noise_level_buffer_size

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
        while True:
            event = self.queue.get()
            self.update_setting(event[0], event[1])
            self.queue.task_done()
            time.sleep(.001)

    def update_setting(self, type, value):
        # as of now we consider the incoming values to be validated before
        if type == 'threshold':
            self.threshold = value
        elif type == 'noise_level_buffer_size':
            difference = value - self.noise_level_buffer_size
            if difference > 0:
                # increase
                self.noise_level_buffer = ([0] * difference) + self.noise_level_buffer
            else:
                # decrease
                self.noise_level_buffer = self.noise_level_buffer[-difference:]
            self.noise_level_buffer_size = value

    def mic_worker(self):
        while True:
            l, data = self.mic.read()

            if l:
                try:
                    current = audioop.rms(data, 2)
                    self.noise_level_buffer = self.noise_level_buffer[1:]
                    self.noise_level_buffer.append(current)
                    avg = sum(self.noise_level_buffer) / len(self.noise_level_buffer)
                    if avg > self.threshold:
                        if not self.sound_on:
                            self.sound_on = True
                            self.led_controller.led_on()
                            self.event_queue.put(['over_volume_threshold', { 'threshold': self.threshold }])
                    else:
                        if self.sound_on:
                            self.sound_on = False
                            self.led_controller.led_off()
                            self.event_queue.put(['below_volume_threshold', { 'threshold': self.threshold }])
                    time.sleep(.001)
                except audioop.error as e:
                    if "{0}".format(e) != "not a whole number of frames":
                        raise e
                    time.sleep(.001)

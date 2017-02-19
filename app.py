## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import pigpio
from RPi import GPIO
import time
from event_publisher import EventPublisher
from screen_controller import ScreenController
from sound_listener import SoundListener

if __name__ == '__main__':

    event_publisher = EventPublisher()
    queue_events = event_publisher.queue

    screen_controller = ScreenController()
    queue_screen = screen_controller.queue

    sound_listener = SoundListener(600, 5000, queue_events)
    queue_listen = sound_listener.queue

    noise_level_buffer = [0] * 5000
    threshold = 600

    re1_clk = 20
    re1_dt = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(re1_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(re1_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    re1_clkLastState = GPIO.input(re1_clk)

    re2_clk = 19
    re2_dt = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(re2_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(re2_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    re2_clkLastState = GPIO.input(re2_clk)

    def update_threshold(step=50):
        global re1_clkLastState
        global screen_controller
        global threshold
        re1_clkState = GPIO.input(re1_clk)
        re1_dtState = GPIO.input(re1_dt)
        if re1_clkState != re1_clkLastState:
            if re1_dtState != re1_clkState:
                threshold += step
            else:
                if threshold >= step:
                    threshold -= step
                else:
                    threshold = 0
            screen_controller.update(0, 0, "THR: {0}".format(threshold))
            queue_listen.put(['threshold', threshold])

        re1_clkLastState = re1_clkState

    def update_noise_level_buffer(time=100):
        global re2_clkLastState
        global noise_level_buffer
        global screen_controller
        re2_clkState = GPIO.input(re2_clk)
        re2_dtState = GPIO.input(re2_dt)
        if re2_clkState != re2_clkLastState:
            if re2_dtState != re2_clkState:
                noise_level_buffer = ([0] * time) + noise_level_buffer
            else:
                if len(noise_level_buffer) >= time+1:
                    noise_level_buffer = noise_level_buffer[time:]
                else:
                    noise_level_buffer = noise_level_buffer[-1:]
            screen_controller.update(1, 0, "NLB: {0}".format(len(noise_level_buffer)))
            queue_listen.put(['noise_level_buffer_size', len(noise_level_buffer)])

        re2_clkLastState = re2_clkState

    while True:
        update_threshold()
        update_noise_level_buffer()
        time.sleep(.001)



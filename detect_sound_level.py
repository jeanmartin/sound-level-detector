## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
from requests_futures.sessions import FuturesSession
import LCD1602
import sys
import getopt
import requests
import pigpio
import json
from RPi import GPIO
import threading
from queue import Queue
import time

def usage():
    print('usage: recordtest.py [-c <card>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    lock = threading.Lock()
    q = Queue()

    session = FuturesSession()

    LCD1602.init(0x27,1)

    card = 'front:CARD=GoMic,DEV=0'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    pi = pigpio.pi()
    led_r = 17
    led_g = 22
    led_b = 24

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

    def write_to_lcd(data):
        row, column, value = data
        with lock:
            LCD1602.write(row, column, "                ")
            LCD1602.write(row, column, value)

    def worker():
        while True:
            item = q.get()
            write_to_lcd(item)
            q.task_done()

    #for i in range(2):
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

    def update_threshold(step=50):
        global re1_clkLastState
        global threshold
        global s
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
            q.queue.clear()
            q.put([0, 0, "THR: {0}".format(threshold)])

        re1_clkLastState = re1_clkState

    def update_noise_level_buffer(time=100):
        global re2_clkLastState
        global noise_level_buffer
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
            q.queue.clear()
            q.put([0, 1, "NLB: {0}".format(len(noise_level_buffer))])

        re2_clkLastState = re2_clkState

    def led_on():
        pi.set_PWM_dutycycle(led_r, 255)
        pi.set_PWM_dutycycle(led_g, 0)
        pi.set_PWM_dutycycle(led_b, 0)

    def led_off():
        pi.set_PWM_dutycycle(led_r, 0)
        pi.set_PWM_dutycycle(led_g, 0)
        pi.set_PWM_dutycycle(led_b, 0)

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, card)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(8000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
    inp.setperiodsize(160)

    led_off()

    max = 0
    noise_level_buffer = [0] * 5000
    threshold = 700
    sound_on = False
    q.put([0, 0, "THR: {0}".format(threshold)])
    q.put([0, 1, "NLB: {0}".format(len(noise_level_buffer))])
    while True:
        # Read data from device
        l,data = inp.read()

        update_threshold()
        update_noise_level_buffer()

        if l:
          try:
            # Return the maximum of the absolute value of all samples in a fragment.
            current = audioop.max(data, 2)
            noise_level_buffer = noise_level_buffer[1:]
            noise_level_buffer.append(current)

            avg = sum(noise_level_buffer) / len(noise_level_buffer)
            if max < current:
              max = current
            if avg > threshold:
              if not sound_on:
                sound_on = True
                led_on()
                session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': 'over_volume_threshold', 'payload': { 'threshold': threshold } } }))
            else:
              if sound_on:
                sound_on = False
                led_off()
                session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': 'below_volume_threshold', 'payload': { 'threshold': threshold } } }))

            print("{0} / {1}".format(threshold, len(noise_level_buffer)))
            time.sleep(.001)
          except audioop.error as e:
            if "{0}".format(e) != "not a whole number of frames":
              raise e


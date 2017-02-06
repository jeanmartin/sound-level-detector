## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
import sys
import getopt
import requests

def usage():
    print('usage: recordtest.py [-c <card>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':

    card = 'front:CARD=GoMic,DEV=0'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

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

    max = 0
    tmp = [0] * 5000
    threshold = 700
    sound_on = false
    while True:
        # Read data from device
        l,data = inp.read()

        if l:
        # Return the maximum of the absolute value of all samples in a fragment.
          current = audioop.max(data, 2)
          tmp = tmp[1:]
          tmp.append(current)

          avg = sum(tmp) / len(tmp)
          if max < current:
            max = current
          if avg > threshold:
            print(current)
            if !sound_on
              sound_on = true
              #requests.post('http://kraken.test.io/events', data={ 'event': 'over_volume_threshold', 'threshold': threshold })
          else
            if sound_on
              sound_on = false
              #requests.post('http://kraken.test.io/events', data={ 'event': 'below_volume_threshold', 'threshold': threshold })

          time.sleep(.001)

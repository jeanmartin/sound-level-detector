import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_input = 1

while True:
    input = GPIO.input(18)
    if (prev_input and (not input)):
        print("Button pressed")
    prev_input = input
    time.sleep(0.02)

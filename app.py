## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import pigpio
from RPi import GPIO
import time
from settings import Settings
from event_publisher import EventPublisher
from screen_controller import ScreenController
from sound_listener import SoundListener
from menu import Menu
from heartbeat import Heartbeat
from distance_measurer import DistanceMeasurer

if __name__ == '__main__':

    event_publisher = EventPublisher()
    queue_events = event_publisher.queue

    Heartbeat(event_publisher)

    screen_controller = ScreenController()

    DistanceMeasurer(screen_controller).start()

    sound_listener = SoundListener(Settings.INITIAL_THRESHOLD, Settings.INITIAL_BUFFER_SIZE, queue_events)
    queue_listen = sound_listener.queue

    menu = Menu(screen_controller, queue_listen)

    # initial state
    menu.update_screen()
    screen_controller.turn_off_light()

    # Rotary Encoder 1 (Menu Select)
    re1_clk = Settings.GPIO['RE_1_CLK']
    re1_dt = Settings.GPIO['RE_1_DT']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(re1_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(re1_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    re1_clkLastState = GPIO.input(re1_clk)

    # Rotary Encoder 2 (Value Change)
    re2_clk = Settings.GPIO['RE_2_CLK']
    re2_dt = Settings.GPIO['RE_2_DT']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(re2_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(re2_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    re2_clkLastState = GPIO.input(re2_clk)

    def update_menu_option():
        global re1_clkLastState
        global screen_controller
        re1_clkState = GPIO.input(re1_clk)
        re1_dtState = GPIO.input(re1_dt)
        if re1_clkState != re1_clkLastState:
            if re1_dtState != re1_clkState:
                # turned right
                menu.next_option()
            else:
                # turned left
                menu.prev_option()
        re1_clkLastState = re1_clkState

    def update_menu_value():
        global re2_clkLastState
        global screen_controller
        re2_clkState = GPIO.input(re2_clk)
        re2_dtState = GPIO.input(re2_dt)
        if re2_clkState != re2_clkLastState:
            if re2_dtState != re2_clkState:
                # turned right
                menu.increase_value()
            else:
                # turned left
                menu.decrease_value()
        re2_clkLastState = re2_clkState

    while True:
        update_menu_option()
        update_menu_value()
        time.sleep(.001)



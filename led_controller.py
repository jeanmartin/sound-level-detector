#!/usr/bin/env python
import pigpio
from RPi import GPIO
from settings import Settings

class LEDController():
    PI = pigpio.pi()
    LED_R = Settings.GPIO['LED_RED']
    LED_G = Settings.GPIO['LED_GREEN']
    LED_B = Settings.GPIO['LED_BLUE']

    def __init__(self):
        self.led_off()

    def led_on(self):
      self.PI.set_PWM_dutycycle(self.LED_R, 255)
      self.PI.set_PWM_dutycycle(self.LED_G, 0)
      self.PI.set_PWM_dutycycle(self.LED_B, 0)

    def led_off(self):
      self.PI.set_PWM_dutycycle(self.LED_R, 0)
      self.PI.set_PWM_dutycycle(self.LED_G, 0)
      self.PI.set_PWM_dutycycle(self.LED_B, 0)

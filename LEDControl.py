#!/usr/bin/env python
import pigpio
from RPi import GPIO

pi = pigpio.pi()
led_r = 17
led_g = 22
led_b = 24

def initialize():
  led_off()

def led_on():
  pi.set_PWM_dutycycle(led_r, 255)
  pi.set_PWM_dutycycle(led_g, 0)
  pi.set_PWM_dutycycle(led_b, 0)

def led_off():
  pi.set_PWM_dutycycle(led_r, 0)
  pi.set_PWM_dutycycle(led_g, 0)
  pi.set_PWM_dutycycle(led_b, 0)

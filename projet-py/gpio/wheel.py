#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

# Gestion PWM
import RPi.GPIO as GPIO

"""
    Classe pour représenter une roue générique
"""

POS_LEFT        =   "POS_LEFT"
POS_RIGHT       =   "POS_RIGHT"

MAX_PWM         =   0.5
MIN_PWM         =   0.3
ROTATION_PWM    =   0.3
DELTA_PWM       =   0.1

VALUE_ON        =   1
VALUE_OFF       =   0

GPIO_MODE_IN    =   "IN"
GPIO_MODE_OUT   =   "OUT"

PWM_FREQUENCY   =   100


class Wheel(object):    
    def __init__(self, log, position, pwm_bcm, in1_wpi, in2_wpi):
        self.pwm_value = MIN_PWM
        self.in1_value = VALUE_OFF
        self.in2_value = VALUE_OFF
        self.position = position
        
        self.pwm_bcm = pwm_bcm
        self.in1_wpi = in1_wpi
        self.in2_wpi = in2_wpi
        
        self.pwm_mode = GPIO_MODE_IN
        self.in1_mode = GPIO_MODE_IN
        self.in2_mode = GPIO_MODE_IN
        
        self.log = log
        
        # Liste de valeurs des WPI pour simplifier la vérification
        # des valeurs modifiées
        self.pin_values = {}
        
        # Gestion PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_bcm, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_bcm, PWM_FREQUENCY)
        self.pwm.start(0.0)
        self.pwm_value = 0.0

        
    def command_gpio_mode(self, wpi, value):
        cmd = "gpio mode " + str(wpi) + " " + value
        self.log.log_debug(cmd)
        os.system(cmd)
        
    def command_gpio_write(self, wpi, value):
        # Si la valeur du pin ne change pas, on ne l'écrit pas
        if (wpi not in self.pin_values
                or self.pin_values[wpi] != value):
            cmd = "gpio write " + str(wpi) + " " + str(value)
            self.log.log_debug(cmd)
            os.system(cmd)
            self.pin_values[wpi] = value

    def change_pwm_mode(self, mode):
        self.log.log_debug("pwm mode " + str(self.pwm_bcm) + " " + str(mode))
        if mode == GPIO_MODE_OUT:
            GPIO.setup(self.pwm_bcm, GPIO.OUT)
        else:
            GPIO.setup(self.pwm_bcm, GPIO.IN)

    def set_pwm(self, value):
        # Si la valeur du pin ne change pas, on ne l'écrit pas
        if self.pwm_value != value:
            self.pwm_value = min(float(value), MAX_PWM)
            self.log.log_debug("pwm value " + str(self.pwm_bcm) + " " + str(self.pwm_value))
            self.pwm.ChangeDutyCycle(self.pwm_value * 100.0)

    def increment_pwm(self):
        if self.pwm_value < MAX_PWM:
            self.set_pwm(self.pwm_value + DELTA_PWM)
        

    def set_all_mode(self, mode):
        self.pwm_mode = self.in1_mode = self.in2_mode = mode
        self.change_pwm_mode(mode)
        self.command_gpio_mode(self.in1_wpi, mode)
        self.command_gpio_mode(self.in2_wpi, mode)

    def set_pin_values(self, pwm, in1, in2):
        self.set_pwm(pwm)
        self.in1_value = in1
        self.in2_value = in2
        self.command_gpio_write(self.in1_wpi, in1)
        self.command_gpio_write(self.in2_wpi, in2)

    def stop(self):
        self.set_pin_values(MIN_PWM, VALUE_OFF, VALUE_OFF)

    def forward(self):
        self.set_pin_values(self.pwm_value, VALUE_OFF, VALUE_ON)

    def backward(self):
        self.set_pin_values(self.pwm_value, VALUE_ON, VALUE_OFF)

    def is_forward(self):
        return self.in2_value == VALUE_ON and self.in1_value == VALUE_OFF

    def is_backward(self):
        return self.in1_value == VALUE_ON and self.in2_value == VALUE_OFF

    def is_rotate_left(self):
        return (self.is_forward() and (self.position == POS_RIGHT)
            or self.is_backward() and (self.position == POS_LEFT))

    def is_rotate_right(self):
        return (self.is_forward() and (self.position == POS_LEFT)
            or self.is_backward() and (self.position == POS_RIGHT))

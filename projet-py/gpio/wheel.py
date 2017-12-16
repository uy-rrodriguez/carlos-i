#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour représenter une roue générique
"""

POS_LEFT        =   "POS_LEFT"
POS_RIGHT       =   "POS_RIGHT"

MAX_PWM         =   0.8
MIN_PWM         =   0.1
DELTA_PWM       =   0.1

VALUE_ON        =   1
VALUE_OFF       =   0

GPIO_MODE_IN    =   "IN"
GPIO_MODE_OUT   =   "OUT"

class Wheel(object):    
    def __init__(self, log, position, pwm_wpi, in1_wpi, in2_wpi):
        self.pwm = MIN_PWM
        self.in1 = VALUE_OFF
        self.in2 = VALUE_OFF
        self.position = position
        
        self.pwm_wpi = pwm_wpi
        self.in1_wpi = in1_wpi
        self.in2_wpi = in2_wpi
        
        self.pwm_mode = GPIO_MODE_IN
        self.in1_mode = GPIO_MODE_IN
        self.in2_mode = GPIO_MODE_IN
        
        self.log = log
        
        # Liste de valeurs des WPI pour simplifier la vérification
        # des valeurs modifiées
        self.wpi_values = {}
        
    def command_gpio_mode(self, wpi, value):
        cmd = "gpio mode " + str(wpi) + " " + value
        self.log.log_debug(cmd)
        #os.system(cmd)
        
    def command_gpio_write(self, wpi, value):
        # Si la valeur du pin ne change pas, on ne l'écrit pas
        if wpi not in self.wpi_values or self.wpi_values[wpi] != value:
            self.wpi_values[wpi] = value
            cmd = "gpio write " + str(wpi) + " " + str(value)
            self.log.log_debug(cmd)
            #os.system(cmd)
        
    def set_all_mode(self, value):
        self.pwm_mode = self.in1_mode = self.in2_mode = value
        self.command_gpio_mode(self.pwm, value)
        self.command_gpio_mode(self.in1, value)
        self.command_gpio_mode(self.in2, value)

    def set_pin_values(self, pwm, in1, in2):
        self.pwm = pwm
        self.in1 = in1
        self.in2 = in2
        self.command_gpio_write(self.pwm_wpi, pwm)
        self.command_gpio_write(self.in1_wpi, in1)
        self.command_gpio_write(self.in2_wpi, in2)

    def set_pwm(self, pwm):
        self.pwm = min(pwm, MAX_PWM)
        self.command_gpio_write(self.pwm_wpi, self.pwm)

    def stop(self):
        self.set_pin_values(self.pwm, VALUE_OFF, VALUE_OFF)

    def forward(self):
        self.set_pin_values(self.pwm, VALUE_OFF, VALUE_ON)

    def backward(self):
        self.set_pin_values(self.pwm, VALUE_ON, VALUE_OFF)

    def is_forward(self):
        return self.in2 == VALUE_ON and self.in1 == VALUE_OFF

    def is_backward(self):
        return self.in1 == VALUE_ON and self.in2 == VALUE_OFF

    def is_rotate_left(self):
        return (self.is_forward() and (self.position == POS_RIGHT)
            or self.is_backward() and (self.position == POS_LEFT))

    def is_rotate_right(self):
        return (self.is_forward() and (self.position == POS_LEFT)
            or self.is_backward() and (self.position == POS_RIGHT))

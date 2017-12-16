#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour contrôler les moteurs via les valeurs des pins GPIO.
"""

import os, time

# Wheels' wPi numbers
FRONT_RIGHT_PWM    =    12
FRONT_RIGHT_IN1    =    13
FRONT_RIGHT_IN2    =    14

FRONT_LEFT_PWM     =    27
FRONT_LEFT_IN1     =    28
FRONT_LEFT_IN2     =    29

BACK_RIGHT_PWM     =    6
BACK_RIGHT_IN1     =    10
BACK_RIGHT_IN2     =    11

BACK_LEFT_PWM      =    0
BACK_LEFT_IN1      =    2
BACK_LEFT_IN2      =    3

MODE_IN            =    "IN"
MODE_OUT           =    "OUT"

VALUE_ON           =    "1"
VALUE_OFF          =    "0"

DIRECTION_FORWARD  =    "FWD"
DIRECTION_BACKWARD =    "BKW"


class Log(object):
    DEBUG = 0
    INFO = 1
    ERROR = 9
    
    def __init__(self, mode=0):
        self.mode = mode
    
    def log(self, text):
        print(text)
    
    def log_info(self, text):
        if self.mode <= Log.INFO:
            self.log(text)
    
    def log_debug(self, text):
        if self.mode <= Log.DEBUG:
            self.log(text)
    
    def log_error(self, text):
        if self.mode <= Log.ERROR:
            self.log(text)


class Wheel(object):
    def __init__(self, gpio_pwm, gpio_in1, gpio_in2):
        self.log = Log(Log.INFO)
        self.pwm = gpio_pwm
        self.in1 = gpio_in1
        self.in2 = gpio_in2
        
        self.pwm_mode = MODE_IN
        self.in1_mode = MODE_IN
        self.in2_mode = MODE_IN
        
        self.pwm_value = VALUE_OFF
        self.in1_value = VALUE_OFF
        self.in2_value = VALUE_OFF
        
    def command_gpio_mode(self, wpi, value):
        cmd = "gpio mode " + str(wpi) + " " + value
        self.log.log_debug(cmd + "\n")
        os.system(cmd)
        
    def command_gpio_write(self, wpi, value):
        cmd = "gpio write " + str(wpi) + " " + value
        self.log.log_debug(cmd + "\n")
        os.system(cmd)
        
    def set_all_mode(self, value):
        self.pwm_mode = self.in1_mode = self.in2_mode = value
        self.command_gpio_mode(self.pwm, value)
        self.command_gpio_mode(self.in1, value)
        self.command_gpio_mode(self.in2, value)

    def set_gpio_values(self, pwm_value, in1_value, in2_value):
        self.pwm_value = pwm_value
        self.in1_value = in1_value
        self.in2_value = in2_value
        self.command_gpio_write(self.pwm, pwm_value)
        self.command_gpio_write(self.in1, in1_value)
        self.command_gpio_write(self.in2, in2_value)


class Robot(object):
    def __init__(self):
        self.log = Log(Log.INFO)
        self.wheels = [
            Wheel(FRONT_LEFT_PWM,   FRONT_LEFT_IN1,  FRONT_LEFT_IN2),
            Wheel(FRONT_RIGHT_PWM,  FRONT_RIGHT_IN1, FRONT_RIGHT_IN2),
            Wheel(BACK_LEFT_PWM,    BACK_LEFT_IN1,   BACK_LEFT_IN2),
            Wheel(BACK_RIGHT_PWM,   BACK_RIGHT_IN1,  BACK_RIGHT_IN2)
        ]
    
    def config(self):
        [w.set_all_mode(MODE_OUT) for w in self.wheels]
    
    def init(self):
        [w.set_gpio_values(VALUE_ON, VALUE_OFF, VALUE_OFF) for w in self.wheels]
    
    def stop(self):
        [w.set_gpio_values(w.pwm_value, VALUE_OFF, VALUE_OFF) for w in self.wheels]
    
    def forward(self):
        [w.set_gpio_values(w.pwm_value, VALUE_OFF, VALUE_ON) for w in self.wheels]
    
    def backward(self):
        [w.set_gpio_values(w.pwm_value, VALUE_ON, VALUE_OFF) for w in self.wheels]
            
            
    def test_fwd_bkw(self):
        self.log.log_info("Test Robot Forward - Backward")
        w = Robot()
        
        self.log.log_debug("Config"); w.config()
        
        self.log.log_debug("Init"); w.init()
        
        self.log.log_debug("Forward"); w.forward(); time.sleep(1)
        
        self.log.log_debug("Stop"); w.stop(); time.sleep(1)
        
        self.log.log_debug("Backward"); w.backward(); time.sleep(1)
        
        self.log.log_debug("Stop"); w.stop()
            
            
    def test_detect(self):
        self.log.log_info("Test Detect Wheels")
        w = Robot()
        w.debug = True
        
        self.log.log_debug("Config"); w.config()
        self.log.log_debug("Init"); w.init()
        
        self.log.log_debug("Front Left -> Forward")
        w.stop()
        self.wheels[0].set_gpio_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Front Right -> Forward")
        w.stop()
        self.wheels[1].set_gpio_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Back Left -> Forward")
        w.stop()
        self.wheels[2].set_gpio_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Back Right -> Forward")
        w.stop()
        self.wheels[3].set_gpio_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Stop"); w.stop()



    ####################################################################
    # Contrôle avancé des moteurs. Gestion de vitesse, démarrage et    #
    # arrêt doux (utilisation du PWM).                                 #
    ####################################################################
    
    def start_wheel(self, wpi, direction, speed):
        self.command_gpio_write(wpi, VALUE_ON)
        
if __name__ == "__main__":
    #Robot().test_fwd_bkw()
    #Robot().test_detect()
    pass

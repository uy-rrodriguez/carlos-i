#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour contrôler les moteurs via les valeurs des pins GPIO.
"""

import os, time
import wheel
from wheel import *


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

KEY_FORWARD        =    "K_FWD"
KEY_BACKWARD       =    "K_BKW"
KEY_LEFT           =    "K_LEFT"
KEY_RIGHT          =    "K_RIGHT"


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

class Robot(object):
    def __init__(self):
        self.log = Log(Log.DEBUG)
        self.wheels = [
            wheel.Wheel(self.log, wheel.POS_LEFT,   FRONT_LEFT_PWM,   FRONT_LEFT_IN1,  FRONT_LEFT_IN2),
            wheel.Wheel(self.log, wheel.POS_RIGHT,  FRONT_RIGHT_PWM,  FRONT_RIGHT_IN1, FRONT_RIGHT_IN2),
            wheel.Wheel(self.log, wheel.POS_LEFT,   BACK_LEFT_PWM,    BACK_LEFT_IN1,   BACK_LEFT_IN2),
            wheel.Wheel(self.log, wheel.POS_RIGHT,  BACK_RIGHT_PWM,   BACK_RIGHT_IN1,  BACK_RIGHT_IN2)
        ]
        
        # Gestion des commandes de mouvement envoyées
        self.keys = {
            KEY_FORWARD:    False,
            KEY_BACKWARD:   False,
            KEY_LEFT:       False,
            KEY_RIGHT:      False
        }

        # Pour gérer le mouvement, on a une direction de déplacement
        # linéaire et un direction de rotation
        self.linear_direction = 0
        self.rotation_direction = 0
    
    def config(self):
        [w.set_all_mode(GPIO_MODE_OUT) for w in self.wheels]
    
    def init(self):
        [w.set_pin_values(VALUE_ON, VALUE_OFF, VALUE_OFF) for w in self.wheels]
    
    def clean(self):
        [w.set_pin_values(VALUE_OFF, VALUE_OFF, VALUE_OFF) and w.set_all_mode(GPIO_MODE_IN) for w in self.wheels]
    
    def on_key_press(self, key):
        self.keys[key] = True
    
    def on_key_release(self, key):
        self.keys[key] = False

    def update(self):
        # Détection de la direction du mouvement
        self.linear_direction = 0
        self.rotation_direction = 0
        
        if self.keys[KEY_FORWARD]:
            self.linear_direction += 1

        if self.keys[KEY_BACKWARD]:
            self.linear_direction -= 1
        
        if self.keys[KEY_LEFT]:
            self.rotation_direction -= 1

        if self.keys[KEY_RIGHT]:
            self.rotation_direction += 1

        
        # Modification des pins des roues
        #[w.stop() for w in self.robot.wheels]
        if self.rotation_direction == 0:
            if self.linear_direction > 0:
                [w.forward() for w in self.wheels]
            elif self.linear_direction < 0:
                [w.backward() for w in self.wheels]
            else:
                [w.stop() for w in self.wheels]
                
        elif self.rotation_direction > 0:
            self.wheels[0].forward()
            self.wheels[2].forward()
            self.wheels[1].backward()
            self.wheels[3].backward()
                
        elif self.rotation_direction < 0:
            self.wheels[0].backward()
            self.wheels[2].backward()
            self.wheels[1].forward()
            self.wheels[3].forward()

    '''
    def stop(self):
        [w.stop() for w in self.wheels]
    
    def forward(self):
        [w.forward() for w in self.wheels]
    
    def backward(self):
        [w.backward() for w in self.wheels]
    '''
            
    def test_fwd_bkw(self):
        self.log.log_info("Test Robot Forward - Backward")
        r = Robot()
        
        self.log.log_debug("Config"); r.config()
        
        self.log.log_debug("Init"); r.init()
        
        self.log.log_debug("Forward"); w.forward(); time.sleep(1)
        
        self.log.log_debug("Stop"); r.stop(); time.sleep(1)
        
        self.log.log_debug("Backward"); r.backward(); time.sleep(1)
        
        self.log.log_debug("Stop"); r.stop()
            
            
    def test_detect(self):
        self.log.log_info("Test Detect Wheels")
        r = Robot()
        r.debug = True
        
        self.log.log_debug("Config"); r.config()
        self.log.log_debug("Init"); r.init()
        
        self.log.log_debug("Front Left -> Forward")
        r.stop()
        self.wheels[0].set_pin_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Front Right -> Forward")
        r.stop()
        self.wheels[1].set_pin_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Back Left -> Forward")
        r.stop()
        self.wheels[2].set_pin_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Back Right -> Forward")
        r.stop()
        self.wheels[3].set_pin_values(VALUE_OFF, VALUE_OFF, VALUE_ON)
        time.sleep(1)
        
        self.log.log_debug("Stop"); r.stop()

        
if __name__ == "__main__":
    #Robot().test_fwd_bkw()
    Robot().test_detect()
    pass

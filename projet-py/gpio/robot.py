#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour contrôler les moteurs via les valeurs des pins GPIO.
"""

import os, time
import wheel
from wheel import *


# Wheels' wPi numbers
FRONT_RIGHT_PWM    =    10 #=BCM #wPi=12
FRONT_RIGHT_IN1    =    13 #=wPi
FRONT_RIGHT_IN2    =    14 #=wPi

FRONT_LEFT_PWM     =    16 #=BCM #wPi=27
FRONT_LEFT_IN1     =    28
FRONT_LEFT_IN2     =    29

BACK_RIGHT_PWM     =    25 #=BCM #wPi=6
BACK_RIGHT_IN1     =    10
BACK_RIGHT_IN2     =    11

BACK_LEFT_PWM      =    17 #=BCM #wPi=0
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
        self.previous_rotation = False
    
    def config(self):
        [w.set_all_mode(GPIO_MODE_OUT) for w in self.wheels]
    
    def init(self):
        [w.set_pin_values(0.0, VALUE_OFF, VALUE_OFF) for w in self.wheels]
    
    def clean(self):
        [w.set_pin_values(0.0, VALUE_OFF, VALUE_OFF) for w in self.wheels]
        [w.set_all_mode(GPIO_MODE_IN) for w in self.wheels]
    
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
        #[w.set_pin_values(w.wpm_value, VALUE_OFF, VALUE_OFF) for w in self.robot.wheels]
        if self.rotation_direction == 0:
            if self.previous_rotation:
                self.previous_rotation = False
                # Restart PWM
                [w.set_pwm(wheel.MIN_PWM) for w in self.wheels]
                
            if self.linear_direction > 0:
                self.forward()
            elif self.linear_direction < 0:
                self.backward()
            else:
                self.stop()
        
        else :
            self.linear_direction = 0
            self.previous_rotation = True
            [w.set_pwm(wheel.MAX_PWM) for w in self.wheels]
            
            if self.rotation_direction > 0:
                self.wheels[0].forward()
                self.wheels[2].forward()
                self.wheels[1].backward()
                self.wheels[3].backward()
                    
            else: #self.rotation_direction < 0:
                self.wheels[0].backward()
                self.wheels[2].backward()
                self.wheels[1].forward()
                self.wheels[3].forward()

    def stop(self):
        [w.stop() for w in self.wheels]
    
    def forward(self):
        [w.forward() for w in self.wheels]
    
    def backward(self):
        [w.backward() for w in self.wheels]
            
    def test_fwd_bkw(self):
        self.log.log_info("Test Robot Forward - Backward")
        
        self.log.log_debug("Config"); self.config()
        
        self.log.log_debug("Init"); self.init()
        
        self.log.log_debug("Forward"); self.forward(); time.sleep(1)
        
        self.log.log_debug("Stop"); self.stop(); time.sleep(1)
        
        self.log.log_debug("Backward"); self.backward(); time.sleep(1)
        
        self.log.log_debug("Stop"); self.stop()

            
            
    def test_detect(self):
        self.log.log_info("Test Detect Wheels")
        
        self.log.log_debug("Config"); self.config()
        self.log.log_debug("Init"); self.init()
        
        self.log.log_debug("Front Left -> Forward")
        self.stop()
        self.wheels[0].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_debug("Front Right -> Forward")
        self.stop()
        self.wheels[1].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_debug("Back Left -> Forward")
        self.stop()
        self.wheels[2].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_debug("Back Right -> Forward")
        self.stop()
        self.wheels[3].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_debug("Stop");
        self.stop()

        
if __name__ == "__main__":
    r = Robot()
    #r.test_fwd_bkw()
    r.test_detect()
        
    r.log.log_debug("Clean");
    r.clean()

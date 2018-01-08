#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour contrôler les moteurs via les valeurs des pins GPIO.
"""

import os, time
import wheel
from wheel import *
from sensor import sensor


# Wheels' pins
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

# Key codes
KEY_FORWARD        =    "K_FWD"
KEY_BACKWARD       =    "K_BKW"
KEY_LEFT           =    "K_LEFT"
KEY_RIGHT          =    "K_RIGHT"

# Sensors' pins
SENSOR_FRONT_TRIG  =    13 #=BCM, wPi=23
SENSOR_FRONT_ECHO  =    5  #=BCM, wPi=21

SENSOR_BACK_TRIG   =    19 #=BCM, wPi=24
SENSOR_BACK_ECHO   =    6  #=BCM, wPi=22

# Obstacle detection
MIN_DISTANCE_FRONT = 10   #=cm
MIN_DISTANCE_BACK  = 15   #=cm


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
        #self.log = Log(Log.DEBUG)
        self.log = Log(Log.INFO)
        #self.log = Log(Log.ERROR)
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
        
        # Pour la détection d'objets, on a deux télémètres, devant et derrière
        self.sensor_front = sensor.Sensor(SENSOR_FRONT_TRIG, SENSOR_FRONT_ECHO)
        self.sensor_back = sensor.Sensor(SENSOR_BACK_TRIG, SENSOR_BACK_ECHO)
        self.sensors = [self.sensor_front, self.sensor_back]
        
        # On peut assigner une caméra après l'initialisation du robot
        self.camera = None
        
    
    def config(self):
        [w.set_all_mode(GPIO_MODE_OUT) for w in self.wheels]
        [s.config() for s in self.sensors]
    
    def init(self):
        [w.set_pin_values(0.0, VALUE_OFF, VALUE_OFF) for w in self.wheels]
        [s.init() for s in self.sensors]
    
    def clean(self):
        [w.set_pin_values(0.0, VALUE_OFF, VALUE_OFF) for w in self.wheels]
        [w.set_all_mode(GPIO_MODE_IN) for w in self.wheels]
        [s.clean() for s in self.sensors]
    
    def on_key_press(self, key):
        self.keys[key] = True
    
    def on_key_release(self, key):
        self.keys[key] = False
    
    
    def is_obstacle(self):
        if self.linear_direction > 0:
            distance = self.sensor_front.read()
            return (distance != sensor.OUT_RANGE
                    and distance <= MIN_DISTANCE_FRONT)
            
        elif self.linear_direction < 0:
            distance = self.sensor_back.read()
            return (distance != sensor.OUT_RANGE
                    and distance <= MIN_DISTANCE_BACK)
                    
        else:
            return False


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
        if self.rotation_direction == 0:
            if self.previous_rotation:
                self.previous_rotation = False
                # Restart PWM
                [w.set_pwm(wheel.MIN_PWM) for w in self.wheels]
            
            # Avancer
            if (self.linear_direction > 0
                    and not self.is_obstacle()):
                self.forward()
            
            # Aller en arrière
            elif (self.linear_direction < 0
                    and not self.is_obstacle()):
                self.backward()
            
            # S'arrêter
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
        
        self.log.log_info("Config"); self.config()
        
        self.log.log_info("Init"); self.init()
        
        self.log.log_info("Stop"); self.stop(); time.sleep(1)
        
        self.log.log_info("Forward"); self.forward(); time.sleep(1)
        
        self.log.log_info("Stop"); self.stop(); time.sleep(1)
        
        self.log.log_info("Backward"); self.backward(); time.sleep(1)
        
        self.log.log_info("Stop"); self.stop()
            
            
    def test_detect_manual(self):
        self.log.log_info("Test Detect Wheels")
        
        self.log.log_info("Config"); self.config()
        self.log.log_info("Init"); self.init()
        
        self.log.log_info("Front Left -> Forward")
        self.stop()
        self.wheels[0].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_info("Front Right -> Forward")
        self.stop()
        self.wheels[1].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_info("Back Left -> Forward")
        self.stop()
        self.wheels[2].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_info("Back Right -> Forward")
        self.stop()
        self.wheels[3].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        raw_input("Press Enter to continue...")
        
        self.log.log_info("Stop");
        self.stop()
            
            
    def test_detect(self):
        self.log.log_info("Test Detect Wheels")
        
        self.log.log_info("Config"); self.config()
        self.log.log_info("Init"); self.init()
        
        self.log.log_info("Front Left -> Forward")
        self.stop()
        self.wheels[0].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        time.sleep(0.5)
        
        self.log.log_info("Front Right -> Forward")
        self.stop()
        self.wheels[1].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        time.sleep(0.5)
        
        self.log.log_info("Back Left -> Forward")
        self.stop()
        self.wheels[2].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        time.sleep(0.5)
        
        self.log.log_info("Back Right -> Forward")
        self.stop()
        self.wheels[3].set_pin_values(MIN_PWM, VALUE_OFF, VALUE_ON)
        time.sleep(0.5)
        
        self.log.log_info("Stop");
        self.stop()

    
    
    # ############################################################### #
    #    Gestion de la caméra                                         #
    #                                                                 #
    # ############################################################### #
    def set_camera(self, camera):
        self.camera = camera
    
    def camera_start_stream(self):
        if self.camera is not None:
            self.camera.start_image_stream()

    def camera_stop_stream(self):
        if self.camera is not None:
            self.camera.stop_image_stream()

    def camera_get_last_frame(self):
        if self.camera is not None:
            return self.camera.get_last_frame()
        else:
            return "Camera non configuree"
    
    
        
if __name__ == "__main__":
    r = Robot()
    #r.test_fwd_bkw()
    r.test_detect()
        
    r.log.log_debug("Clean");
    r.clean()

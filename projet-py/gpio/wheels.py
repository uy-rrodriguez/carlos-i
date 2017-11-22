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


class Wheels:
    def __init__(self):
        self.debug = False
        
    def command_gpio_mode(self, wpi, value):
        cmd = "gpio mode " + str(wpi) + " " + value
        if self.debug:
            print(cmd + "\n")
        os.system(cmd)
        
    def command_gpio_write(self, wpi, value):
        cmd = "gpio write " + str(wpi) + " " + value
        if self.debug:
            print(cmd + "\n")
        os.system(cmd)
    
    def config(self):
        wpis = [
            # configure front right wheel
            FRONT_RIGHT_PWM,    FRONT_RIGHT_IN1,    FRONT_RIGHT_IN2,
            
            # configure front left wheel
            FRONT_LEFT_PWM,     FRONT_LEFT_IN1,     FRONT_LEFT_IN2,
            
            # configure back right wheel
            BACK_RIGHT_PWM,     BACK_RIGHT_IN1,     BACK_RIGHT_IN2,
            
            # configure back left wheel
            BACK_LEFT_PWM,      BACK_LEFT_IN1,      BACK_LEFT_IN2]
        
        for wpi in wpis:
            self.command_gpio_mode(wpi, MODE_OUT)
    
    
    def init(self):
        wpis_on = [
            FRONT_RIGHT_PWM,    FRONT_LEFT_PWM,
            BACK_RIGHT_PWM,     BACK_LEFT_PWM]
        
        for wpi in wpis_on:
            self.command_gpio_write(wpi, VALUE_ON)

            
        wpis_off = [
            FRONT_RIGHT_IN1,    FRONT_RIGHT_IN2,
            FRONT_LEFT_IN1,     FRONT_LEFT_IN2,
            BACK_RIGHT_IN1,     BACK_RIGHT_IN2,
            BACK_LEFT_IN1,      BACK_LEFT_IN2]
        
        for wpi in wpis_off:
            self.command_gpio_write(wpi, VALUE_OFF)
    
    
    def stop(self):
        wpis_off = [
            FRONT_RIGHT_IN1,    FRONT_RIGHT_IN2,
            FRONT_LEFT_IN1,        FRONT_LEFT_IN2,
            BACK_RIGHT_IN1,        BACK_RIGHT_IN2,
            BACK_LEFT_IN1,        BACK_LEFT_IN2]
        
        for wpi in wpis_off:
            self.command_gpio_write(wpi, VALUE_OFF)
    
    
    def forward(self):
        wpis_on = [
            FRONT_RIGHT_IN2,    FRONT_LEFT_IN2,
            BACK_RIGHT_IN2,        BACK_LEFT_IN2]
            
        wpis_off = [
            FRONT_RIGHT_IN1,    FRONT_LEFT_IN1,
            BACK_RIGHT_IN1,        BACK_LEFT_IN1]

        for wpi in wpis_on:
            self.command_gpio_write(wpi, VALUE_ON)
        
        for wpi in wpis_off:
            self.command_gpio_write(wpi, VALUE_OFF)
    
    
    def backward(self):
        wpis_on = [
            FRONT_RIGHT_IN1,    FRONT_LEFT_IN1,
            BACK_RIGHT_IN1,     BACK_LEFT_IN1]
            
        wpis_off = [
            FRONT_RIGHT_IN2,    FRONT_LEFT_IN2,
            BACK_RIGHT_IN2,        BACK_LEFT_IN2]
        
        for wpi in wpis_on:
            self.command_gpio_write(wpi, VALUE_ON)
        
        for wpi in wpis_off:
            self.command_gpio_write(wpi, VALUE_OFF)
            
            
    def test_fwd_bkw(self):
        print("Test Wheels Forward - Backward")
        w = Wheels()
        w.debug = True
        
        print("Config"); w.config()
        
        print("Init"); w.init()
        
        print("Forward"); w.forward(); time.sleep(2)
        
        print("Stop"); w.stop(); time.sleep(2)
        
        print("Backward"); w.backward(); time.sleep(2)
        
        print("Stop"); w.stop()
            
            
    def test_detect(self):
        print("Test Detect Wheels")
        w = Wheels()
        w.debug = True
        
        print("Config"); w.config()
        print("Init"); w.init()
        
        print("Front Right -> Forward")
        w.stop()
        self.command_gpio_write(FRONT_RIGHT_IN2, VALUE_ON)
        time.sleep(2)
        
        print("Front Left -> Forward")
        w.stop()
        self.command_gpio_write(FRONT_LEFT_IN2, VALUE_ON)
        time.sleep(2)
        
        print("Back Right -> Forward")
        w.stop()
        self.command_gpio_write(BACK_RIGHT_IN2, VALUE_ON)
        time.sleep(2)
        
        print("Back Left -> Forward")
        w.stop()
        self.command_gpio_write(BACK_LEFT_IN2, VALUE_ON)
        time.sleep(2)
        
        print("Stop"); w.stop()



    ####################################################################
    # Contrôle avancé des moteurs. Gestion de vitesse, démarrage et    #
    # arrêt doux (utilisation du PWM).                                 #
    ####################################################################
    
    def start_wheel(self, wpi, direction, speed):
        self.command_gpio_write(wpi, VALUE_ON)
        
if __name__ == "__main__":
    #Wheels().test_fwd_bkw()
    Wheels().test_detect()

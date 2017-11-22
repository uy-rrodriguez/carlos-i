#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot@alumni.univ-avignon.fr>

"""
    Classe pour contrôler les capteurs ultrason via les valeurs des pins GPIO.
"""

import os

# Sensor 1 wPi numbers
SENSOR_1_IN     =   21
SENSOR_2_IN     =   22

# Sensor 2 wPi numbers
SENSOR_1_OUT    =   13
SENSOR_2_OUT    =   19

class Sensor:
    
    def __init__(self, gpio_in, gpio_out):
        self.gpio_in = gpio_in
        self.gpio_out = gpio_out
        
    def configure(self):
        cmd = "gpio mode " + str(self.gpio_in) + " in"
        print(cmd)
        os.system(cmd)
        cmd = "gpio mode " + str(self.gpio_out) + " out"
        print(cmd)
        os.system(cmd)
        
    def write_to(self, value):
        cmd = "gpio write " + str(self.gpio_out) + " " + value
        print(cmd)
        os.system(cmd);
        
    def get_from(self):
        pass

if __name == "__main__":
    
    print("Front sensor's initialization")
    sensor_1 = Sensor(SENSOR_1_IN, SENSOR_1_OUT)
    
    print("Front sensor's configuration")
    sensor_1.configure()
    
    print("Back sensor's initialization")
    sensor_2 = Sensor(SENSOR_2_IN, SENSOR_2_OUT)
    
    print("Back sensor's configuration")
    sensor_2.configure()
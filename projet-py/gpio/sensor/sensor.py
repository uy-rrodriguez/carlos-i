#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot@alumni.univ-avignon.fr>

"""
    Classe pour contrôler les capteurs ultrason via les valeurs des pins GPIO.
"""

import os, time
from multiprocessing import Process

# Front sensor wPi numbers
FRONT_SENSOR_IN     =   21
BACK_SENSOR_IN      =   22

# Back sensor wPi numbers
FRONT_SENSOR_OUT    =   13
BACK_SENSOR_OUT     =   19

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
        cmd = "gpio write " + str(self.gpio_out) + " " + str(value)
        print(cmd)
        os.system(cmd);
        
    def get_from(self):
        cmd = "gpio read " + str(self.gpio_in)
        print(cmd)
        return os.popen(cmd).read()
        
def send_echo(sensor):
    sensor.write_to(1)
    time.sleep(1)
    sensor.write_to(0)
        
def get_distance(sensor):
    Process(target=send_echo, args=(sensor,)).start()
    echo = 0
    while echo == 0:
        echo = sensor.get_from()
    distance = 0
    while echo == 1:
        distance += 1
        echo = sensor.get_from()
    return distance

if __name__ == "__main__":
    
    print("Front sensor's initialization")
    front_sensor = Sensor(FRONT_SENSOR_IN, FRONT_SENSOR_OUT)
    
    print("Front sensor's configuration")
    front_sensor.configure()
    
    print("Back sensor's initialization")
    back_sensor = Sensor(BACK_SENSOR_IN, BACK_SENSOR_OUT)
    
    print("Back sensor's configuration")
    back_sensor.configure()
    
    print("Distance from front sensor")
    front_distance = get_distance(front_sensor)
    print("Front distance: " + str(front_distance))
    
    print("Distance from back sensor")
    back_distance = get_distance(back_sensor)
    print("Back distance: " + str(back_distance))

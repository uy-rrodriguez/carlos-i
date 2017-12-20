#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour contrôler les télémètres via les valeurs des pins GPIO.
    
    Devant :
        TRIG = GPIO 13 => Mode OUT      Phys. 33    wPi 23  BCM 13
        ECHO = GPIO 05 => Mode IN       Phys. 29    wPi 21  BCM 5
        
    Derrière :
        TRIG = GPIO 19 => Mode OUT      Phys. 35    wPi 24  BCM 19
        ECHO = GPIO 06 => Mode IN       Phys. 31    wPi 22  BCM 6
"""

import time, traceback
import RPi.GPIO as GPIO                    #Import GPIO library


# Limites dans la détection
MIN_RANGE = 2
MAX_RANGE = 400
CALIBRATION = 0.5
PULSE_MULTIPLIER = 17150    #Multiply pulse duration by 17150 to get distance

# Valeur out of range
OUT_RANGE = None

class Sensor(object):
    def __init__(self, pin_trigger, pin_echo):
        self.trigger = pin_trigger
        self.echo = pin_echo

    def config(self):
        GPIO.setmode(GPIO.BCM)                  #Set GPIO pin numbering
        GPIO.setup(self.trigger, GPIO.OUT)      #Set pin as GPIO out
        GPIO.setup(self.echo, GPIO.IN)          #Set pin as GPIO in
        
    def init(self):
        GPIO.output(self.trigger, False)
    
    def clean(self):
        GPIO.output(self.trigger, False)
        GPIO.setup(self.trigger, GPIO.IN)
        
        GPIO.setup(self.echo, GPIO.OUT)
        GPIO.output(self.echo, False)
        GPIO.setup(self.echo, GPIO.IN)
        
    def read(self):
        try:
            GPIO.output(self.trigger, True)         #Set TRIG as HIGH
            time.sleep(0.00001)                     #Delay of 0.00001 seconds
            GPIO.output(self.trigger, False)        #Set TRIG as LOW

            while GPIO.input(self.echo) == 0:      #Check whether the ECHO is LOW
                pulse_start = time.time()           #Saves the last known time of LOW pulse

            while GPIO.input(self.echo) == 1:      #Check whether the ECHO is HIGH
                pulse_end = time.time()             #Saves the last known time of HIGH pulse 

            pulse_duration = pulse_end - pulse_start    #Get pulse duration to a variable

            distance = pulse_duration * PULSE_MULTIPLIER       
            distance = round(distance, 2)           #Round to two decimal points

            if distance > MIN_RANGE and distance < MAX_RANGE: #Check whether the distance is within range
                return distance - CALIBRATION     #Print distance with X cm calibration
            else:
                return OUT_RANGE                         # Out of range

        except:
            traceback.print_exc()
            return OUT_RANGE


    """
    while True:

    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    print "Waitng For Sensor To Settle"
    time.sleep(2)                            #Delay of 2 seconds

    GPIO.output(self.trigger, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(self.trigger, False)                 #Set TRIG as LOW

    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)            #Round to two decimal points

    if distance > 2 and distance < 400:      #Check whether the distance is within range
    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
    else:
    print "Out Of Range"                   #display out of range
    """

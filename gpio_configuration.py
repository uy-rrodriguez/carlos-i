#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot--ribeyre@alumni.univ-avignon.fr>

"""
This script initializes GPIO's configuration by setting
branches to out-mode.
"""

import os

if __name__ == "__main__":
    
    # front right wheel
    os.system("gpio mode 11 out") # PWM
    os.system("gpio mode 13 out") # IN1
    os.system("gpio mode 15 out") # IN2
    
    # back left wheel
    os.system("gpio mode 14 out") # PWM
    os.system("gpio mode 21 out") # IN1
    os.system("gpio mode 23 out") # IN2
    
    # back right wheel
    os.system("gpio mode 36 out") # PWM
    os.system("gpio mode 38 out") # IN1
    os.system("gpio mode 40 out") # IN2
    
    # front left wheel
    os.system("gpio mode 22 out") # PWM
    os.system("gpio mode 24 out") # IN1
    os.system("gpio mode 26 out") # IN2
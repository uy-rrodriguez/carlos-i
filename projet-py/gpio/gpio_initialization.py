#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot@alumni.univ-avinon.fr>

"""
"""

import os

if __name__ == "__main__":

    # initialize front right wheel
    os.system("gpio write 0 1") # PWM
    os.system("gpio write 2 0") # IN1
    os.system("gpio write 3 0") # IN2

    # initialize back left wheel
    os.system("gpio write 12 1") # PWM
    os.system("gpio write 13 0") # IN1
    os.system("gpio write 14 0") # IN2

    # initialize back right wheel
    os.system("gpio write 27 1") # PWM
    os.system("gpio write 28 0") # IN1
    os.system("gpio write 29 0") # IN2

    # initialize front left wheel
    os.system("gpio write 6 1") # PWM
    os.system("gpio write 10 0") # IN1
    os.system("gpio write 11 0") # IN2

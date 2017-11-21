#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot@alumni.univ-avinon.fr>

"""
"""

import os

if __name__ == "__main__":

    # stop front right wheel
    os.system("gpio write 2 0") # IN1
    os.system("gpio write 3 0") # IN2

    # stop back left wheel
    os.system("gpio write 13 0") # IN1
    os.system("gpio write 14 0") # IN2

    # stop back right wheel
    os.system("gpio write 28 0") # IN1
    os.system("gpio write 29 0") # IN2

    # stop front left wheel
    os.system("gpio write 10 0") # IN1
    os.system("gpio write 11 0") # IN2

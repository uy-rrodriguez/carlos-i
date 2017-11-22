#! /usr/bin/python
# -*- coding: utf-8 -*-

# Author: Baptiste BRIOT--RIBEYRE
# <baptiste.briot@alumni.univ-avinon.fr>

"""
"""

import os

if __name__ == "__main__":

    # run front right wheel
    os.system("gpio write 2 1") # IN1
    os.system("gpio write 3 0") # IN2

    # run back left wheel
    os.system("gpio write 13 1") # IN1
    os.system("gpio write 14 0") # IN2

    # run back right wheel
    os.system("gpio write 28 1") # IN1
    os.system("gpio write 29 0") # IN2

    # run front left wheel
    os.system("gpio write 10 1") # IN1
    os.system("gpio write 11 0") # IN2

#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
from threading import Thread

"""
    Thread pour incrémenter le PWM à intervalles réguliers.
"""
class UpdatePWM(Thread):

    def __init__(self, robot):
        self.robot = robot
        self.stopped = False
        super(UpdatePWM, self).__init__()
    
    def run(self):
        while not self.stopped:
            if self.robot.linear_direction != 0:
                [w.increment_pwm() for w in self.robot.wheels]
            self.robot.update()
            time.sleep(0.5) #time.sleep(0.1)

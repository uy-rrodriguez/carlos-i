#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Script de base pour lancer tous les modules du robot.
"""

import sys, traceback

#from gpio.wheel import Wheel
from gpio.robot import Robot
from ws.ws import *
from pwm.pwm import UpdatePWM
from camera.camera import Camera


# ############################################################### #
#    Main                                                         #
#                                                                 #
# ############################################################### #

def main():
    status = 0
    
    robot = None
    webservice = None
    threadPWM = None
    cam = None
    
    try:
        # Création d'un objet pour accéder à la caméra
        cam = Camera()
        
        # Création d'un objet pour accéder au vrai robot
        robot = Robot()
        robot.config()
        robot.init()
        robot.test_detect()
        #self.robot.test_fwd_bkw()
        
        # Assignation de la caméra au robot
        robot.set_camera(cam)
        
        # Création du thread pour incrémenter le PWM
        threadPWM = UpdatePWM(robot)
        threadPWM.start()
        
        # Démarrage du webservice
        webservice = MonWebservice(robot, globals())
        webservice.run()

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        traceback.print_exc()
        status = 1


    # Arrêt du thread pour le PWM
    try:
        if threadPWM != None:
            threadPWM.stopped = True
    except:
        traceback.print_exc()
        status = 1


    # Nettoyage des données du robot
    try:
        if robot != None:
            robot.clean()
    except:
        traceback.print_exc()
        status = 1
    
    
    sys.exit(status)


if __name__ == "__main__":
    sys.exit(main())

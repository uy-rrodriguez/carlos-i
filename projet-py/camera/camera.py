#! /usr/bin/python
# -*- coding: utf-8 -*-

import os


IMAGE_PATH = "/tmp/carlos-i-camera"

"""
    Classe pour contrôler la caméra, prendre des photos et vidéos,
    configurer des prises vidéos à intervalles réguliers et détecter
    des objets.
"""
class Camera(object):
    def __init__(self, dest_path):
        self.dest_path = dest_path
        
        # Suppression du répertoire temporaire
        if os.path.exists(self.dest_path):
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        
        # Création du répertoire temporaire
        if not os.path.exists(self.dest_path):
            os.mkdir(self.dest_path)


    def capture_image(self):
        cmd = "gpio mode " + str(wpi) + " " + value
        self.log.log_debug(cmd)
        os.system(cmd)

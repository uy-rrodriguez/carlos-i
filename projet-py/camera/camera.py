#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time, subprocess
from threading import Thread


# Paramètres pour la capture d'images
CAMERA_IMG_PATH         = "/tmp/carlos_i_images/"
CAMERA_IMG_NAME         = "stream.jpg" #"stream%02d.jpg"
CAMERA_IMG_WIDTH        = 640   # Paramètre -w
CAMERA_IMG_HEIGHT       = 480   # Paramètre -h
CAMERA_IMG_QUALITY      = 5     # Paramètre -q (0 à 100)
CAMERA_IMG_FPS          = 2     # Nombre de photos par seconde
CAMERA_IMG_COMMAND      = "raspistill"
CAMERA_IMG_PARAMS       = "--nopreview -w %i -h %i -q %i -o %s"


"""
    Classe pour contrôler la caméra, prendre des photos et vidéos,
    configurer des prises vidéos à intervalles réguliers et détecter
    des objets.
"""
class Camera(object):
    def __init__(self, dest_path=CAMERA_IMG_PATH):
        self.dest_path = dest_path
        self.create_dest_path()
        self.image_stream = CameraImageStream(self)
    
    def create_dest_path(self):
        # Suppression du répertoire temporaire
        if os.path.exists(self.dest_path):
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        
        # Création du répertoire temporaire
        if not os.path.exists(self.dest_path):
            return os.mkdir(self.dest_path)

        return True

    def start_image_stream(self):
        if self.image_stream.stopped:
            self.image_stream.start()

    def stop_image_stream(self):
        if not self.image_stream.stopped:
            self.image_stream.stop()

    def get_last_frame(self):
        output = self.camera.dest_path + CAMERA_IMG_NAME
        if os.path.exists(output):
            return output
        else
            return ""

"""
    Thread pour gérer un flux d'images.
    
    Quand le flux est activé, on lance une commande raspistill pour prendre
    des photos à intervalles réguliers.
    
    Si le flux est désactivé, il faut arrêter la commande raspistill. Pour cela,
    on utilise une instance de la classe subprocess.Popen qui va faire l'appel
    système et, quand le flux est arrêté, on execute terminate() sur le subprocess.
"""
def CameraImageStream(Thread):
    def __init__(self, camera):
        self.camera = camera
        self.stopped = True
        self.process = None
        super(CameraImageStream, self).__init__()
    
    def run(self):
        self.stopped = False
        
        # Paramètres de base pour une image
        output = self.camera.dest_path + CAMERA_IMG_NAME
        params = CAMERA_IMG_PARAMS % (CAMERA_IMG_WIDTH,
                                       CAMERA_IMG_HEIGHT,
                                       CAMERA_IMG_QUALITY,
                                       output)

        # Paramètres pour lancer raspistill en mode timelapse
        timelapse = int(1000 / CAMERA_IMG_FPS)  # Temps en une photo et la prochaine, en ms
        timeout = 9999999                       # Temps pendant lequel la caméra reste allumée
                                                #   pour continuer à prendre des photos
        params += " -tl %i -t %i" % (timelapse, timeout)
        
        # Création d'un subprocess avec Popen
        cmd = [CAMERA_IMG_COMMAND, params]
        print "LOG [CameraImageStream] :", cmd[0], cmd[1]
        
        self.process = subprocess.Popen(cmd,
                                        stdout=subprocess.STDOUT,
                                        stderr=subprocess.STDOUT)

    def stop(self):
        print "LOG [CameraImageStream] : Trying to stop raspistill"
        if self.process is not None:
            self.process.terminate()
            self.process = None

        self.stopped = True

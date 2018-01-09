#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time, shlex, subprocess
from threading import Thread


# Paramètres pour la capture d'images
CAMERA_IMG_PATH         = "/tmp/carlos_i_images/"
CAMERA_IMG_NAME         = "stream.jpg" #"stream%02d.jpg"
CAMERA_IMG_WIDTH        = 320 #640   # Paramètre -w
CAMERA_IMG_HEIGHT       = 240 #480   # Paramètre -h
CAMERA_IMG_QUALITY      = 5          # Paramètre -q (0 à 100)
CAMERA_IMG_FPS          = 10         # Nombre de photos par seconde
CAMERA_IMG_COMMAND      = "raspistill"
CAMERA_IMG_ARGS         = "--nopreview -w %i -h %i -q %i -o %s"


"""
    Classe pour contrôler la caméra, prendre des photos et vidéos,
    configurer des prises vidéos à intervalles réguliers et détecter
    des objets.
"""
class Camera(object):

    def __init__(self):
        self.create_dest_path(CAMERA_IMG_PATH)
        self.image_stream = CameraImageStream()
    
    def create_dest_path(self, dest_path):
        # Suppression du répertoire temporaire
        if False and os.path.exists(dest_path):
            for root, dirs, files in os.walk(dest_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        
        # Création du répertoire temporaire
        if not os.path.exists(dest_path):
            return os.mkdir(dest_path)

        return True

    def start_image_stream(self):
        if self.image_stream.stopped:
            self.image_stream.start()

    def stop_image_stream(self):
        if not self.image_stream.stopped:
            self.image_stream.stop()

    def get_last_frame(self):
        output = CAMERA_IMG_PATH + CAMERA_IMG_NAME
        #print "LOG [Camera] output :", output
        if os.path.exists(output):
            return output
        else:
            return ""



"""
    Thread pour gérer un flux d'images.
    
    Quand le flux est activé, on lance une commande raspistill pour prendre
    des photos à intervalles réguliers.
    
    Si le flux est désactivé, il faut arrêter la commande raspistill. Pour cela,
    on utilise une instance de la classe subprocess.Popen qui va faire l'appel
    système et, quand le flux est arrêté, on execute terminate() sur le subprocess.
"""
class CameraImageStream(Thread):

    def __init__(self):
        self.stopped = True
        self.command_process = None
        super(CameraImageStream, self).__init__()
    
    def run(self):
        self.stopped = False
        
        # Paramètres de base pour une image
        #output = self.cam.dest_path + CAMERA_IMG_NAME
        output = CAMERA_IMG_PATH + CAMERA_IMG_NAME
        args = CAMERA_IMG_ARGS % (CAMERA_IMG_WIDTH,
                                    CAMERA_IMG_HEIGHT,
                                    CAMERA_IMG_QUALITY,
                                    output)

        # Paramètres pour lancer raspistill en mode timelapse
        timelapse = int(1000 / CAMERA_IMG_FPS)  # Temps en une photo et la prochaine, en ms
        timeout = 30000#9999999                       # Temps pendant lequel la caméra reste allumée
                                                #   pour continuer à prendre des photos
        args += " -tl %i -t %i" % (timelapse, timeout)
        
        # Ligne avec la  commande
        cmd_line = CAMERA_IMG_COMMAND + " " + args
        
        # Division des arguments à envoyer à Popen
        cmd = shlex.split(cmd_line)
        
        while not self.stopped:
            # Création d'un subprocess avec Popen
            print "LOG [CameraImageStream] :", cmd_line
            self.command_process = subprocess.Popen(cmd)
            self.command_process.wait()
            self.command_process = None
            time.sleep(0.0001)

    def stop(self):
        self.stopped = True

        print "LOG [CameraImageStream] : Trying to stop raspistill"
        if self.command_process is not None:
            self.command_process.terminate()
            self.command_process = None


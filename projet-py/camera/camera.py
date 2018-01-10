#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time, shlex, subprocess
from threading import Thread
from shutil import copyfile
from cameratensorflow import CameraTensorFlow

# Paramètres pour la capture d'images
CAMERA_IMG_PATH         = "/tmp/carlos_i_images/"
CAMERA_IMG_NAME         = "stream.jpg" #"stream%02d.jpg"
CAMERA_IMG_WIDTH        = 320 #640   # Paramètre -w
CAMERA_IMG_HEIGHT       = 240 #480   # Paramètre -h
CAMERA_IMG_QUALITY      = 50         # Paramètre -q (0 à 100)
CAMERA_IMG_ROTATION     = 270        # Paramètre -rot
CAMERA_IMG_FPS          = 15         # Nombre de photos par seconde
CAMERA_IMG_COMMAND      = "raspistill"
CAMERA_IMG_ARGS         = "--nopreview -w %i -h %i -rot %i -q %i -o %s"


# Paramètres pour l'analyse d'images
CAMERA_PROCESSING_FILE  = "/tmp/carlos_i_images/processing.jpg"


"""
    Classe pour contrôler la caméra, prendre des photos et vidéos,
    configurer des prises vidéos à intervalles réguliers et détecter
    des objets.
    
    
    Documentation raspistill
        https://www.modmypi.com/blog/raspberry-pi-camera-board-raspistill-command-list
    
    Capture vidéo + Streaming VLC
        raspivid -o - -rot 270 -t 0 -w 640 -h 360 -fps 25|cvlc stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264
    
    Capture images en continu
        raspistill --nopreview -w 320 -h 240 -q 50 -o /tmp/carlos_i_images/stream.jpg -tl 100 -t 0
"""
class Camera(object):

    def __init__(self):
        self.create_dest_path(CAMERA_IMG_PATH)
        self.image_stream = None
        self.image_processor = CameraTensorFlow()
    
    def create_dest_path(self, dest_path):
        # Suppression du répertoire temporaire
        deleteContent = True
        if deleteContent and os.path.exists(dest_path):
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
        if self.image_stream is None:
            self.image_stream = CameraImageStream()
            self.image_stream.start()

    def stop_image_stream(self):
        if self.image_stream is not None:
            self.image_stream.stop()
            self.image_stream = None

    def get_last_frame(self):
        output = CAMERA_IMG_PATH + CAMERA_IMG_NAME
        if os.path.exists(output):
            return output
        else:
            return ""

    def start_processing(self):
        frame = self.get_last_frame()
        #frame = "/home/pi/carlos-i/tensorflow/test.jpg"
        if frame != "":
            copyfile(frame, CAMERA_PROCESSING_FILE)
            self.image_processor.process_image(CAMERA_PROCESSING_FILE)

    def stop_processing(self):
        self.image_processor.stop_process_image()

    def get_processing_result(self):
        return self.image_processor.get_last_result()



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
        self.command_process = None
        super(CameraImageStream, self).__init__()
    
    def run(self):
        # Paramètres de base pour une image
        #output = self.cam.dest_path + CAMERA_IMG_NAME
        output = CAMERA_IMG_PATH + CAMERA_IMG_NAME
        args = CAMERA_IMG_ARGS % (CAMERA_IMG_WIDTH,
                                    CAMERA_IMG_HEIGHT,
                                    CAMERA_IMG_ROTATION,
                                    CAMERA_IMG_QUALITY,
                                    output)

        # Paramètres pour lancer raspistill en mode timelapse
        timelapse = int(1000 / CAMERA_IMG_FPS)  # Temps en une photo et la prochaine, en ms
        timeout = 30000#9999999                 # Temps pendant lequel la caméra reste allumée
                                                #   pour continuer à prendre des photos
        args += " -tl %i -t 0" % (timelapse)
        
        # Ligne avec la  commande
        cmd_line = CAMERA_IMG_COMMAND + " " + args
        
        # Division des arguments à envoyer à Popen
        cmd = shlex.split(cmd_line)
        
        # La sortie sera redirigée à /dev/null
        DEVNULL = open(os.devnull, "w")
        
        # Création d'un subprocess avec Popen
        print "LOG [CameraImageStream] :", cmd_line
        self.command_process = subprocess.Popen(cmd,
                                                stdout=DEVNULL,
                                                stderr=subprocess.STDOUT)
        self.command_process.wait()

    def stop(self):
        print "LOG [CameraImageStream] : Trying to stop raspistill"
        if self.command_process is not None:
            self.command_process.kill()
            self.command_process.wait()


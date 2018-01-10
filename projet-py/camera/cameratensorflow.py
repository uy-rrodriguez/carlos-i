#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, traceback
import time, shlex, subprocess
import re
from threading import Thread, Lock


CAMERA_TF_COMMAND      = "python /home/pi/carlos-i/tensorflow/imagenet/classify_image.py"
CAMERA_TF_MODEL_DIR    = "/home/pi/tensorflow/models/inception/"
CAMERA_TF_PREDICTIONS  = 1

"""
    Classe pour lancer la reconnaissance d'images via TensorFlow.
    
    On utilise un thread séparé qui va rendre le résultat à la fin.
"""
class CameraTensorFlow(object):

    def __init__(self):
        self.inner_thread = None
        self.last_result = None
        self.lock_result = Lock()
    
    def process_image(self, image):
        self.last_result = "Processing..."
        self.inner_thread = CameraTensorFlowThread(image, self)
        self.inner_thread.start()
    
    def stop_process_image(self):
        if self.inner_thread is not None and self.inner_thread.is_alive():
            #self.inner_thread.stop()
            
            # Le stop est fait par un troisème thread pour ne pas
            # bloquer l'option l'application faisant l'appel, mais
            # pouvoir toujours attendre la fermeture du subprocess
            t = Thread(target=self.inner_thread.stop)
            t.start()
            
        self.inner_thread = None
    
    def set_last_result(self, result):
        self.last_result = result
    
    def get_last_result(self):
        return self.last_result
        
        

"""
    Thread pour faire l'appel système de la reconnaissance d'images.
    
    Un subprocess sera créé pour reconnaître l'objet devant la caméra,
    qui pourra être arrêté à tout moment.
    
    Guide basique TensorFlow
        https://www.tensorflow.org/get_started/get_started
"""        
class CameraTensorFlowThread(Thread):
    def __init__(self, image, parent):
        self.image = image
        self.parent = parent
        self.command_process = None
        super(CameraTensorFlowThread, self).__init__()
    
    def run(self):
        # Lock result modifications
        self.parent.lock_result.acquire()
        
        # Start subprocess and wait for result
        self.start_subprocess(self.image)
        result = self.read_subprocess()
        
        # Write result on parent's attribute
        self.parent.set_last_result(result)
        
        # Lock release
        self.parent.lock_result.release()
        
    
    def stop(self):
        print "LOG [CameraTensorFlow] : Stop called"
        self.stop_subprocess()
        self.parent.lock_result.acquire()
        self.parent.set_last_result(None)
        self.parent.lock_result.release()
        
        
    def start_subprocess(self, image):
        cmd_line = CAMERA_TF_COMMAND
        cmd_line += ' --model_dir "%s"' % (CAMERA_TF_MODEL_DIR)
        cmd_line += ' --num_top_predictions %i' % (CAMERA_TF_PREDICTIONS)
        cmd_line += ' --image_file "%s"' % (image)
        
        cmd = shlex.split(cmd_line)
        
        # La sortie d'erreur sera redirigée à /dev/null
        DEVNULL = open(os.devnull, "w")
        
        # Création d'un subprocess avec Popen
        print "LOG [CameraTensorFlow] :", cmd_line
        self.command_process = subprocess.Popen(cmd,
                                                stdout=subprocess.PIPE,
                                                stderr=DEVNULL)
        
    def parse_result(self, result):
        lines = result.split("\n")
        for l in lines:
            match = re.search('^(.*) \(score = .*\)$', l)
            if match:
                return match.group(1)
        return None
    
    def read_subprocess(self):
        if self.command_process is not None:
            print "LOG [CameraTensorFlow] : Waiting result from tensorflow"
            self.command_process.wait()
            result = self.command_process.stdout.read()
            print "LOG [CameraTensorFlow] : Result tensorflow", result
            return self.parse_result(result)
        else:
            return None
        
    def stop_subprocess(self):
        print "LOG [CameraTensorFlow] : Trying to stop tensorflow"
        if self.command_process is not None:
            self.command_process.kill()
            self.command_process.wait()
            
    
def main():
    status = 0
    
    try:
        start = time.time()
        image = "/home/pi/carlos-i/tensorflow/examples/test.jpg"
        
        cameraTF = CameraTensorFlow()
        
        # Création du processus pour analyser l'image
        cameraTF.process_image(image)
        
        # Test stop process image
        #time.sleep(2)
        #cameraTF.stop_process_image()
        
        # Lecture du resultat
        cameraTF.inner_thread.join()
        result = cameraTF.get_last_result()
        
        end = time.time()
        
        print "Time: %i seconds" % (end - start)
        print result

    except:
        traceback.print_exc()
        status = 1
    
    sys.exit(status)


if __name__ == "__main__":
    sys.exit(main())

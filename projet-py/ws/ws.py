#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
    Classe pour publier un service web qui recevra des commandes.
    Les commandes seront ensuite envoyées au robot.
    
    Un thread parallèle permet d'actualiser le PWM des roues à
    intervalles réguliers.
"""

import os, sys, traceback, json
import base64
import web
import gpio.robot


# ############################################################### #
#    Configuration                                                #
#                                                                 #
# ############################################################### #


# IP et port par défaut
DEFAULT_IP = "10.3.141.1"
DEFAULT_PORT = 8080

# Formats d'URLs acceptées
URLS = (
    "/command/press/(.*)",      "Press",
    "/command/release/(.*)",    "Release",
    
    "/stream",                  "ImageStream",
    "/stream/(start|stop)",     "ImageStreamControl",
    "/stream/htmlviewer",       "ImageStreamViewer",
    "/stream/htmlviewer/jquery.js", "ImageStreamViewerJQuery",
    
    "/recognition/(start|stop)", "RecognitionControl",

    "/(.*)",                    "NotFound"
)

# Touches acceptées
WS_KEY_UP       = "forward"
WS_KEY_DOWN     = "backward"
WS_KEY_LEFT     = "left"
WS_KEY_RIGHT    = "right"

# Formats d'image reconnus
IMAGE_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "gif": "image/gif",
    "ico": "image/x-icon"            
}



# ############################################################### #
#    Classes pour traiter les requêtes                            #
#                                                                 #
# ############################################################### #


# -- MonWebservice ---------------------------------------------- #
'''
    Hérite de web.application pour étendre ses fonctionnalités
'''
class MonWebservice(web.application, object):
    instance = None
    robot = None
    threadPWM = None
    translate_keys = None

    def __init__(self, robot, vars_globals):
        super(MonWebservice, self).__init__(URLS, vars_globals)
        MonWebservice.instance = self
        
        self.robot = robot
        
        # Traduction de touches reçues à commandes du robot
        self.translate_keys = {
            WS_KEY_UP:      gpio.robot.KEY_FORWARD,
            WS_KEY_DOWN:    gpio.robot.KEY_BACKWARD,
            WS_KEY_LEFT:    gpio.robot.KEY_LEFT,
            WS_KEY_RIGHT:   gpio.robot.KEY_RIGHT,
        }
        

    def run(self, ip=DEFAULT_IP, port=DEFAULT_PORT, *middleware):
        func = self.wsgifunc(*middleware)
        serv = web.httpserver.runsimple(func, (ip, port))
        return serv
        


# -- Press -------------------------------------------- #

'''
    Appuie sur une touche de mouvement.
'''
class Press:
    def GET(self, data):
        inst = MonWebservice.instance
        try:
            if data in inst.translate_keys:
                inst.robot.on_key_press(inst.translate_keys[data])
                return "OK"
            else:
                return "KEY NOT FOUND"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e

            

# -- Release ------------------------------------------ #

'''
    Arrêt d'appuie sur une touche de mouvement.
'''
class Release:
    def GET(self, data):
        inst = MonWebservice.instance
        try:
            if data in inst.translate_keys:
                inst.robot.on_key_release(inst.translate_keys[data])
                return "OK"
            else:
                return "KEY NOT FOUND"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e

            

# -- ImageStream -------------------------------------- #

'''
    Récupération d'un stream en forme de flux d'images.
    
    La méthode GET va retourner l'objet JSON suivant :
        {
            "response": {
                "stream": "<image encodé en Base64>",
                "recognition": "<string vide>" ou "<objet reconnu>"
            }
        }
'''
class ImageStream:
    def GET(self):
        inst = MonWebservice.instance
        try:
            img = inst.robot.camera_get_last_frame()
            ext = img.split(".")[-1]
            
            if os.path.exists(img):
                #web.header("Content-Type", IMAGE_TYPES[ext]) # Header pour renvoyer une image
                #return open(img, "rb").read()                # On ouvre l'image et on retourne le binaire, 'rb'
                
                # Conversion de l'image à texte
                image_base64 = ""
                with open(img, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read())
                
                # Obtention de l'objet reconnu par la caméra
                recognition = inst.robot.camera_get_processing_result()
                if recognition is None:
                    recognition = ""
                
                # Construction de l'objet JSON résultant
                response = '{"response":{'
                response += '"stream":"' + image_base64 + '",'
                response += '"recognition":"' + recognition + '"'
                response += '}}'
                
                return response
                
            else:
                #return "Image '%s' non trouvée ou stream inactif" % (img)
                return web.NoContent(data="Image '%s' non trouvée ou stream inactif" % (img))

        except Exception as e:
            traceback.print_exc()
            #return "%s" % e
            return web.InternalError("%s" % e)

            

# -- ImageStreamControl ------------------------------- #

'''
    Activation ou désactivation du stream d'images.
'''
class ImageStreamControl:
    def GET(self, cmd):
        inst = MonWebservice.instance
        try:
            if cmd == "start":
                inst.robot.camera_start_stream()
                return "Stream started"
                
            elif cmd == "stop":
                inst.robot.camera_stop_stream()
                return "Stream stopped"
                
            else:
                return "Command '%s' not found" % (cmd)

        except Exception as e:
            traceback.print_exc()
            return "%s" % e

            

# -- ImageStreamViewer -------------------------------- #

'''
    Activation ou désactivation du stream d'images.
'''
class ImageStreamViewer:
    def GET(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "htmlviewer", "htmlviewer.html"), "r") as viewer:
            return viewer.read()



# -- ImageStreamViewerJQuery -------------------------- #

'''
    Bibliothueque JQuery pour le HTMLViewer.
'''
class ImageStreamViewerJQuery:
    def GET(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "htmlviewer", "jquery-3.2.1.min.js"), "r") as jquery:
            return jquery.read()
            


# -- RecognitionControl ------------------------------- #

'''
    Démarrage et arrêt de la reconnaissance d'images.
'''
class RecognitionControl:
    def GET(self, cmd):
        inst = MonWebservice.instance
        try:
            if cmd == "start":
                inst.robot.camera_start_processing()
                return "Recognition started"
                
            elif cmd == "stop":
                inst.robot.camera_stop_processing()
                return "Recognition stopped"
                
            else:
                return "Command '%s' not found" % (cmd)

        except Exception as e:
            traceback.print_exc()
            return "%s" % e
            
            

# -- NotFound --------------------------------------------- #

'''
    Traitement d'une URL qui ne correspond a aucune autre règle.
'''
class NotFound:
    def response(self):
        return web.notfound()

    def GET(self, data):
        return self.response()

    def POST(self, data):
        return self.response()

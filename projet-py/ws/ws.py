# coding: utf8

import sys, traceback, json
import ws.web
import gpio


# ############################################################### #
#    Configuration                                                #
#                                                                 #
# ############################################################### #


# IP et port par défaut
DEFAULT_IP = "10.3.141.1"
DEFAULT_PORT = 8080

# Formats d'URLs acceptées
urls = (
    "/command/config",      "Config",
    "/command/init",        "Init",
    "/command/start",       "Forward",
    "/command/stop",        "Stop",
    "/(.*)",                "NotFound"
)

# Variable qui va stocker l'instance du WS (sera de type MonWebservice)
instanceWS = None



# ############################################################### #
#    Classes pour traiter les requêtes                            #
#                                                                 #
# ############################################################### #


# -- MonWebservice ---------------------------------------------- #
'''
    Hérite de web.application pour étendre ses fonctionnalités
'''
class MonWebservice(ws.web.application, object):
    instance = None

    def __init__(self, urls, vars_globals):
        super(MonWebservice, self).__init__(urls, vars_globals)
        MonWebservice.instance = self

    def run(self, ip=DEFAULT_IP, port=DEFAULT_PORT, *middleware):
        func = self.wsgifunc(*middleware)
        serv = ws.web.httpserver.runsimple(func, (ip, port))
        return serv



# -- Config --------------------------------------------- #

'''
    Configuration des modes (OUT) des pins GPIO.
'''
class Config:
    def GET(self):
        try:
            w = gpio.wheels.Wheels()
            w.config()
            return "OK"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e


# -- Init --------------------------------------------- #

'''
    Initialisation des valeurs pour les GPIO concernés.
'''
class Init:
    def GET(self):
        try:
            w = gpio.wheels.Wheels()
            w.init()
            return "OK"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e


# -- Forward --------------------------------------------- #

'''
    Démarrage des moteurs, le robot avance.
'''
class Forward:
    def GET(self):
        try:
            w = gpio.wheels.Wheels()
            w.forward()
            return "OK"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e


# -- Backward --------------------------------------------- #

'''
    Démarrage des moteurs, le robot va en arrière.
'''
class Backward:
    def GET(self):
        try:
            w = gpio.wheels.Wheels()
            w.backward()
            return "OK"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e


# -- Stop --------------------------------------------- #

'''
    Le robot s'arrete complètement.
'''
class Stop:
    def GET(self):
        try:
            w = gpio.wheels.Wheels()
            w.stop()
            return "OK"

        except Exception as e:
            traceback.print_exc()
            return "%s" % e


# -- NotFound --------------------------------------------- #

'''
    Traitement d'une URL qui ne correspond a aucune autre règle.
'''
class NotFound:
    def response(self):
        return "404"

    def GET(self, data):
        return self.response()

    def POST(self, data):
        return self.response()



# ############################################################### #
#    Main                                                         #
#                                                                 #
# ############################################################### #

def main():
    status = 0
    try:
        # Démarrage du webservice
        instanceWS = MonWebservice(urls, globals())
        instanceWS.run(ip=DEFAULT_IP, port=DEFAULT_PORT)

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        traceback.print_exc()
        status = 1

    sys.exit(status)


if __name__ == "__main__":
    sys.exit(main())

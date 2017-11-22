# coding: utf8

import sys, traceback, json
import web
import gpio


# ############################################################### #
#    Configuration                                                #
#                                                                 #
# ############################################################### #


# Formats d'URLs acceptées
urls = (
	"/command/config",		"ConfigGPIO",
	"/command/init",		"InitGPIO",
	"/command/start",		"Forward",
    "/phrase/stop",         "Stop",
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
class MonWebservice(web.application, object):
    instance = None

    def __init__(self, urls, vars_globals):
        super(MonWebservice, self).__init__(urls, vars_globals)
        MonWebservice.instance = self

    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        serv = web.httpserver.runsimple(func, ('0.0.0.0', port))
        print_()
        return serv



# -- ConfigGPIO --------------------------------------------- #

'''
    Configuration des modes (OUT) des pins GPIO.
'''
class ConfigGPIO:
    def GET(self):
        try:
            w = gpio.proxy.commandeVocale(parole)

                # Reponse
                reponse = {}
                reponse["commande"] = c.commande
                reponse["erreur"] = c.erreur
                reponse["msgErreur"] = c.msgErreur
                reponse["retour"] = c.retour

            else:
                reponse["msgErreur"] = "Erreur de connection au serveur Manager"

            return json.dumps(reponse)

        except Exception, e:
            print_exc_()

            reponse = {"erreur" : True,
                       "msgErreur" : "%s" % e,
                       "commande" : "", "retour" : ""}
            return json.dumps(reponse)


# -- CommandePhrase --------------------------------------------- #

'''
    Traitement d'une commande vocale émulée avec des phrases depuis Android.
    On va recevoir le string représentant la phrase prononcée par l'utilisateur.
'''
class CommandePhrase:
    def GET(self, phrase):
        web.header('Content-Type', 'application/json')

        reponse = {"erreur" : True,
                   "msgErreur" : "Erreur inconnue",
                   "commande" : "", "retour" : ""}

        try:
            if (ManagerProxy.proxy and ManagerProxy.proxy != None):
                # Appel
                c = ManagerProxy.proxy.commandePhrase(phrase)
                print c
                
                # Reponse
                reponse = {}
                reponse["commande"] = c.commande
                reponse["erreur"] = c.erreur
                reponse["msgErreur"] = c.msgErreur
                reponse["retour"] = c.retour

            else:
                reponse["msgErreur"] = "Erreur de connection au serveur Manager"

            return json.dumps(reponse)

        except Exception, e:
            print_exc_()

            reponse = {"erreur" : True,
                       "msgErreur" : "%s" % e,
                       "commande" : "", "retour" : ""}
            return json.dumps(reponse)


# -- CommandeManuelle ------------------------------------------- #

'''
    Traitement d'une commande manuelle.
    On va recevoir la commande et le nom du fichier audio correspondant.
'''
class CommandeManuelle:
    def GET(self, commande, param1=None):
        web.header('Content-Type', 'application/json')

        reponse = {"erreur" : True,
                   "msgErreur" : "Erreur inconnue",
                   "commande" : "", "retour" : ""}

        try:
            if (ManagerProxy.proxy and ManagerProxy.proxy != None):
                # Création de l'objet Commande
                c = AppMP3Player.Commande()
                c.commande = commande

                if (param1 != None):
                    c.params = [param1]
                else:
                    c.params = []

                # Appel
                c = ManagerProxy.proxy.commandeManuelle(c)

                # Reponse
                reponse = {}
                reponse["commande"] = c.commande
                reponse["erreur"] = c.erreur
                reponse["msgErreur"] = c.msgErreur
                reponse["retour"] = c.retour

            else:
                reponse["msgErreur"] = "Erreur de connection au serveur Manager"

            return json.dumps(reponse)

        except Exception, e:
            print_exc_()

            reponse = {"erreur" : True,
                       "msgErreur" : "%s" % e,
                       "commande" : "", "retour" : ""}
            return json.dumps(reponse)


# -- NotFound --------------------------------------------- #

'''
    Traitement d'une URL qui ne correspond a aucune autre regle.
'''
class NotFound:
    def reponse(self):
        reponse = {"erreur" : True,
                   "msgErreur" : "URL incorrecte",
                   "commande" : "", "retour" : ""}
        return json.dumps(reponse)

    def GET(self, data):
        return self.reponse()

    def POST(self, data):
        return self.reponse()



# ############################################################### #
#    Main                                                         #
#                                                                 #
# ############################################################### #

def main():
    status = 0
    ic = None
    try:
        props = Ice.createProperties(sys.argv)
        iniData = Ice.InitializationData()
        iniData.properties = props

        # Initialisation du serveur et Ice
        ic = Ice.initialize(iniData)
        base = ic.stringToProxy("Manager:default -h " + config.IP_MANAGER + " -p " + str(config.PORT_ICE_MANAGER))
        manager = AppMP3Player.ManagerPrx.checkedCast(base)
        if not manager:
            raise RuntimeError("Invalid proxy")


        # On stocke le proxy dans une instance de ManagerProxy
        ManagerProxy(manager)

        # Publication de l'IP du WS
        reponse_ip, erreur_ip = set_public_ip()
        if not reponse_ip:
            print_("Erreur lors de la publication de l'IP du WS. " + erreur_ip)


        # Démarrage du webservice
        instanceWS = MonWebservice(urls, globals())
        instanceWS.run(port=int(config.PORT_WS))

    except (KeyboardInterrupt, SystemExit):
        pass

    except:
        print_exc_()
        status = 1

    if ic:
        # Clean up
        try:
            ic.destroy()
        except:
            print_exc_()
            status = 1

    sys.exit(status)


if __name__ == "__main__":
    sys.exit(main())

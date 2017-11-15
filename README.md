# carlos-i
Carlos-I, une plate-forme robotique pour la détection autmatique d'objets.
CERI. Université d'Avignon 2017-2018.

## Cahier de charges
https://e-uapv2017.univ-avignon.fr/pluginfile.php/5566/mod_resource/content/3/CDC_RobotMobile_ILSEN_V08Sep17.pdf

## Serveur DHCP
Carlos-I aura le rôle de point d'accès WiFi qui nous permettra de nous connecter directement depuis l'application Android. Nous avons configuré un serveur DHCP suivant le guide :
https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software

## TensorFlow by Google :
### Installation
Problème rencontré, les binaires Python par défaut proposés ar Google sont pour 64 bits.
https://stackoverflow.com/questions/33752772/tensorflow-on-raspberry-pi

Solution, installation de binaires alternatifs comilés exprès pour Raspberry PI 3 et l'OS Rapsbian.
https://github.com/samjabrahams/tensorflow-on-raspberry-pi

### Utilisation
Exemle sur l'entrainement et l'utilisation de TensorFlow.
https://www.svds.com/tensorflow-image-recognition-raspberry-pi/

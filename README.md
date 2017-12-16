<div style="text-align:center"><img src="https://github.com/uy-rrodriguez/carlos-i/blob/master/logo/logo.png" height="200px" alt="Logo Carlos-I"/></div>

# carlos-i
Carlos-I, une plate-forme robotique pour la détection autmatique d'objets.
CERI. Université d'Avignon 2017-2018.

## Cahier de charges
https://e-uapv2017.univ-avignon.fr/pluginfile.php/5566/mod_resource/content/3/CDC_RobotMobile_ILSEN_V08Sep17.pdf

## Serveur DHCP
Carlos-I aura le rôle de point d'accès WiFi qui nous permettra de nous connecter directement depuis l'application Android. Nous avons configuré un serveur DHCP suivant le guide :
https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-softwar

Possibilité d'utiliser RaspAP (???).

## TensorFlow by Google :
### Installation
Problème rencontré, les binaires Python par défaut proposés ar Google sont pour 64 bits.
https://stackoverflow.com/questions/33752772/tensorflow-on-raspberry-pi

Solution, installation de binaires alternatifs comilés exprès pour Raspberry PI 3 et l'OS Rapsbian.
https://github.com/samjabrahams/tensorflow-on-raspberry-pi

### Utilisation
Exemle sur l'entrainement et l'utilisation de TensorFlow.
https://www.svds.com/tensorflow-image-recognition-raspberry-pi/

## Gestion de projet
Utilisation des méthodes AGILE (Kanban).
### Taiga.io
https://tree.taiga.io/project/baptistebr-carlos-i/

## GPIO
### Configuration
Pour chaque :

    (1) GPIO
    
    (2) Phys.
    
    (3) wPI

PWM | IN1 | IN2

17:11:0 | 27:13:2 | 22:15:3 | AVD

10:14:12 | 9:21:13 | 11:23:14 | ARG

16:36:27 | 20:38:28 | 21:40:29 | ARD

25:22:6 | 8:24:10 | 7:26:11 | AVG


Avancer :

    IN1=1

    IN2=0
#### Commandes (exemple)
    gpio readall

    gpio mode 11 out

    gpio mode 13 out

    gpio mode 15 out

    gpio write 0 1

    gpio write 2 0

    gpio write 3 1 // wpm

## Caméra
### Cature d'images
raspistill -o image.jpeg

### Cature et conversion de vidéos
https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md

#### Installer l'util MP4Box
sudo apt-get install -y gpac

#### Etapes
\# Capture 30 seconds of raw video at 640x480 and 150kB/s bit rate into a pivideo.h264 file

raspivid -t 30000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264 

\# Wrap the raw video with an MP4 container

MP4Box -add pivideo.h264 pivideo.mp4

\# Remove the source raw file, leaving the remaining pivideo.mp4 file to play

rm pivideo.h264

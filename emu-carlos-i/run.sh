#!/usr/bin/env sh

# Configuration du path de pyglet
set OLD_PYTHONPATH $PYTHONPATH
export PYTHONPATH=$(pwd)/modules/:$PYTHONPATH

# Lancement de l'application
#python main.py
python -m main

# Retour au normal
export PYTHONPATH=$OLD_PYTHONPATH

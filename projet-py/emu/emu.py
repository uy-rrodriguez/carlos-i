#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pyglet
import emurobot

# Path vers les ressources
pyglet.resource.path = ['./emu/resources']
pyglet.resource.reindex()


# Création de l'objet window principal
game_window = pyglet.window.Window(800, 600, resizable=False)

# Chargement des images
robot_image = pyglet.resource.image("robot.png")
robot_image.anchor_x = robot_image.width // 2
robot_image.anchor_y = robot_image.height // 2


# Objet Batch pour contenir les éléments à afficher
main_batch = pyglet.graphics.Batch()


# Création du sprite avec le robot
robot_sprite = emurobot.Robot(img=robot_image, x=400, y=300, batch=main_batch)

# Traitement des événements par l'objet du robot
game_window.push_handlers(robot_sprite)
#game_window.push_handlers(robot_sprite.key_handler)


# Textes sur l'écran
title_label = pyglet.text.Label(text="Emulateur Carlos-I", x=400, y=580,
                                anchor_x='center', anchor_y='baseline',
                                color=(200, 200, 255, 255),
                                batch=main_batch)


# Liste d'objets à actualiser
game_objects = [robot_sprite]


# Evénement on_draw
@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


# Actualisation d'objets
def update(dt):
    for obj in game_objects:
        obj.update(dt)

def run():
    # Appel de la méthode update 120 fois par séconde
    # 120 = 2 * 60 (60 Hz est le taux de rafraîchissement max. typique des écrans)
    pyglet.clock.schedule_interval(update, 1/120.0)
    
    # Initialisation de l'application
    pyglet.app.run()
    
if __name__ == '__main__':
    run()

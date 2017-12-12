#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pyglet
import physicalobject


# Path vers les images
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

# Création de l'objet window principal
game_window = pyglet.window.Window(800, 600, resizable=False)

# Chargement des images
robot_image = pyglet.resource.image("robot.png")

# Fonction pour centrer images
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2

center_image(robot_image)


# Objet Batch pour contenir les éléments à afficher
main_batch = pyglet.graphics.Batch()


# Création du sprite avec le robot
robot_sprite = physicalobject.PhysicalObject(img=robot_image, x=400, y=300,
                                    batch=main_batch)


# Textes sur l'écran
title_label = pyglet.text.Label(text="Emulateur Carlos-I", x=400, y=580,
                                anchor_x='center', anchor_y='baseline',
                                color=(200, 200, 255, 255),
                                batch=main_batch)


# Evénement on_draw
@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()




if __name__ == '__main__':
    pyglet.app.run()

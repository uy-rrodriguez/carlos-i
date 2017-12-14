#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pyglet
import physicalobject

from pyglet.window import key

import math

# Importation des ressources
#import resources


class Wheel(object):
    def __init__(self):
        self.pwd = 0
        self.p1 = 0
        self.p2 = 0

    def set_pins(self, pwd, p1, p2):
        self.pwd = pwd
        self.p1 = p1
        self.p2 = p2

    def forward(self):
        self.set_pins(self.pwd, 1, 0)

    def backward(self):
        self.set_pins(seld.pwd, 0, 1)

    def set_pwd(self, pwd):
        self.pwd == pwd


class Robot(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        #self.default_speed = 10
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.rotation = -90.0
        self.velocity_coeff = 50
        #self.default_angle_radians = 0.0 #-90.0
        #self.keys = dict(left=False, right=False, up=False, down=False)
        self.key_handler = key.KeyStateHandler()

        self.wheels = [Wheel(), Wheel(), Wheel(), Wheel()]

        # Gestion du PWD
        self.max_pwd_freq = 10
    
    def on_key_press(self, symbol, modifiers):
        pass
        '''
        if symbol == key.UP:
            self.keys[‘up’] = True
        elif symbol == key.DOWN:
            self.keys[‘down’] = True
        elif symbol == key.LEFT:
            self.keys[‘left’] = True
        elif symbol == key.RIGHT:
            self.keys[‘right’] = True
        '''

    def on_key_release(self, symbol, modifiers):
        pass
        '''
        if symbol == key.UP:
            self.keys[‘up’] = False
        elif symbol == key.DOWN:
            self.keys[‘down’] = False
        elif symbol == key.LEFT:
            self.keys[‘left’] = False
        elif symbol == key.RIGHT:
            self.keys[‘right’] = False
        '''

    def update(self, dt):
        # self.t stocke le temps passé depuis la dernière fois qu'on a envoyé un TOP de PWD
        # À chaque update, on va donc réduire le temps donné par dt
        if self.t > 0 : self.t -= dt

        # A chaque update, PWD passe de nouveau à zéro
        [w.set_pwd(0) for w in self.wheels]

        if self.key_handler[key.UP]:
            # Pour avancer, on change les pins des roues et on augmente la fréquence du PWD
            [w.forward() for w in self.wheels]

            # On contrôle la fréquence de PWD, si on a atteint le temps d'attente, on remet PWD à 1
            if (self.t <= 0):
                [w.set_pwd(1) for w in self.wheels]

            #angle_radians = -math.radians(self.rotation)
            #force_x = math.cos(angle_radians) * self.thrust * dt
            #force_y = math.sin(angle_radians) * self.thrust * dt
            #self.velocity_x = self.velocity_coeff * force_x
            #self.velocity_y = self.velocity_coeff * force_y
        else:
            #self.velocity_x = self.velocity_y = 0

        # Vérification de la direction du mouvement
        if self.key_handler[key.LEFT]: #self.keys['left']: #and not self.keys['right']:
            #self.velocity_x = -self.default_speed
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]: #and not self.keys['left']:
            #self.velocity_x = self.default_speed
            self.rotation += self.rotate_speed * dt

        #elif self.keys['up'] and not self.keys['down']:
        #    self.velocity_y = self.default_speed
        #elif self.keys['down'] and not self.keys['up']:
        #    self.velocity_y = -self.default_speed

        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x = self.velocity_coeff * force_x
            self.velocity_y = self.velocity_coeff * force_y
        else:
            self.velocity_x = self.velocity_y = 0

        super(Player, self).update(dt)


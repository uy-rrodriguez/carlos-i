#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import pyglet
import physicalobject

from pyglet.window import key
from gpio import wheel
from gpio import robot


LINEAR_SPEED = 15.0 #100.0
ROTATION_SPEED = 13.0 #30.0

class Robot(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)

        self.rotation = -90.0
        self.velocity_coeff = 50
        #self.key_handler = key.KeyStateHandler()
        
        # Gestion du pwm. On va faire appel à la fonction d'actualisation
        # du PWM toutes les N secondes
        pyglet.clock.schedule_interval(self.update_pwm, 0.1) #1 seconde / 10
        
        # Création d'un objet pour accéder au vrai robot
        self.robot = robot.Robot()
        self.robot.config()
        self.robot.init()
        #self.robot.test_detect()
        self.robot.test_fwd_bkw()
        
        # Traduction de touches du clavier à commandes du robot
        self.translate_keys = {
            key.UP:     robot.KEY_FORWARD,
            key.DOWN:   robot.KEY_BACKWARD,
            key.LEFT:   robot.KEY_LEFT,
            key.RIGHT:  robot.KEY_RIGHT,
        }
    
    def on_key_press(self, symbol, modifiers):
        if symbol in self.translate_keys:
            self.robot.on_key_press(self.translate_keys[symbol])

    def on_key_release(self, symbol, modifiers):
        if symbol in self.translate_keys:
            self.robot.on_key_release(self.translate_keys[symbol])

    def update_pwm(self, dt):
        '''
        # Si on ne bouge plus, le PWM revient à zéro
        if self.robot.linear_direction == 0 and self.robot.rotation_direction == 0:
            [w.set_pwm(wheel.MIN_PWM) for w in self.robot.wheels]
        
        elif self.robot.rotation_direction != 0:
            [w.set_pwm(wheel.MAX_PWM) for w in self.robot.wheels]
        
        # Si on se déplace, le PWM va augmenter petit à petit
        else:
            [w.increment_pwm() for w in self.robot.wheels]
        '''
        if self.robot.linear_direction != 0:
            [w.increment_pwm() for w in self.robot.wheels]

    
    def get_linear_speed(self, w):
        if w.is_forward():      dir = 1
        elif w.is_backward():   dir = -1
        else:                   dir = 0
        
        return dir * w.pwm_value * LINEAR_SPEED
    
    def get_rotation_speed(self, w):
        if w.is_forward():      dir = 1
        elif w.is_backward():   dir = -1
        else:                   dir = 0
        
        if w.position == wheel.POS_LEFT:
            return dir * wheel.MAX_PWM * ROTATION_SPEED
        elif w.position == wheel.POS_RIGHT:
            return -1 * dir * wheel.MAX_PWM * ROTATION_SPEED


    def update(self, dt):
        self.robot.update()
        
        # Calcul du mouvement simulé par rapport aux valeurs des roues :
        # Chaque roue apporte une force vers l'avant ou l'arrière par
        # rapport à la valeur de ses pins, plus une rotation horaire ou
        # anti-horaire.
        #
        # Ex.: roue 1 (devant-gauche), si sa direction va vers l'avant
        # (in1 = 1, in2 = 0), elle apporte une force vers l'avant et une
        # rotation horaire.
        linear_speed = 0
        rotation_speed = 0
        for w in self.robot.wheels:
            # Calcul vitesse linéaire
            linear_speed += self.get_linear_speed(w)
            
            # Calcul vitesse de rotation
            rotation_speed += self.get_rotation_speed(w)
        

        # Actualisation de la position par rapport aux vitesses
        
        # Rotation de l'image
        self.rotation += rotation_speed * dt
        
        # Avancement de l'image
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * linear_speed * dt
        force_y = math.sin(angle_radians) * linear_speed * dt
        self.velocity_x = self.velocity_coeff * force_x
        self.velocity_y = self.velocity_coeff * force_y

        super(Robot, self).update(dt)


    def clean(self):
        self.robot.clean()



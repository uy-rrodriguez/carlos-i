#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pyglet
import physicalobject
import robot

from pyglet.window import key

import math

# Importation des ressources
#import resources


class Wheel(object):
    POS_LEFT = "POS_LEFT"
    POS_RIGHT = "POS_RIGHT"
    LINEAR_SPEED = 15.0
    ROTATION_SPEED = 13.0
    MAX_PWM = 0.8
    MIN_PWM = 0.1
    DELTA_PWM = 0.1
    
    def __init__(self, position):
        self.pwm = Wheel.MIN_PWM
        self.p1 = 0
        self.p2 = 0
        self.position = position

    def set_pins(self, pwm, p1, p2):
        self.pwm = pwm
        self.p1 = p1
        self.p2 = p2

    def set_pwm(self, pwm):
        self.pwm = min(pwm, Wheel.MAX_PWM)

    def stop(self):
        self.set_pins(self.pwm, 0, 0)

    def forward(self):
        self.set_pins(self.pwm, 1, 0)

    def backward(self):
        self.set_pins(self.pwm, 0, 1)

    def is_forward(self):
        return (self.p1 - self.p2) == 1

    def is_backward(self):
        return (self.p2 - self.p1) == 1

    def is_rotate_left(self):
        return (self.is_forward() and (self.position == Wheel.POS_RIGHT)
            or self.is_backward() and (self.position == Wheel.POS_LEFT))

    def is_rotate_right(self):
        return (self.is_forward() and (self.position == Wheel.POS_LEFT)
            or self.is_backward() and (self.position == Wheel.POS_RIGHT))
    
    def get_linear_speed(self):
        return (self.p1 - self.p2) * self.pwm * Wheel.LINEAR_SPEED
    
    def get_rotation_speed(self):
        if self.position == Wheel.POS_LEFT:
            return (self.p1 - self.p2) * Wheel.MAX_PWM * Wheel.ROTATION_SPEED
        elif self.position == Wheel.POS_RIGHT:
            return (self.p2 - self.p1) * Wheel.MAX_PWM * Wheel.ROTATION_SPEED


class Player(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.rotation = -90.0
        self.velocity_coeff = 50
        self.key_handler = key.KeyStateHandler()

        self.wheels = [Wheel(Wheel.POS_LEFT),
                       Wheel(Wheel.POS_RIGHT),
                       Wheel(Wheel.POS_LEFT),
                       Wheel(Wheel.POS_RIGHT)]

        # Pour gérer le mouvement, on a une direction de déplacement
        # linéaire et un direction de rotation
        self.linear_direction = 0
        self.rotation_direction = 0
        
        # Gestion du pwm. On va faire appel à la fonction d'actualisation
        # du PWM toutes les N secondes
        pyglet.clock.schedule_interval(self.update_pwm, 0.1) #1 seconde / 10
        
        # Création d'un objet pour accéder au vrai robot
        self.robot = robot.Robot()
        #self.robot.test_detect()
        #self.robot.test_fwd_bkw()
        #self.robot.config()
        #self.robot.init()
    
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


    def set_robot_gpio(self):
        # Transformation de l'information simulée en valeurs GPIO
        for i in range(4):
            pwm = robot.VALUE_ON #self.wheels[i].pwm
            in1 = robot.VALUE_ON if self.wheels[i].p2 == 1 else robot.VALUE_OFF
            in2 = robot.VALUE_ON if self.wheels[i].p1 == 1 else robot.VALUE_OFF
            
            self.robot.wheels[i].set_gpio_values(pwm, in1, in2)


    def update_pwm(self, dt):
        # Si on ne bouge plus, le PWM revient à zéro
        if self.linear_direction == 0 or self.rotation_direction != 0:
            [w.set_pwm(Wheel.MIN_PWM) for w in self.wheels]
        
        # Si on bouge, le PWM va augmenter petit à petit
        else:
            [w.set_pwm(w.pwm + Wheel.DELTA_PWM) for w in self.wheels]
            
        #print [w.pwm for w in self.wheels]

        
    def update(self, dt):
        # Détection de la direction du mouvement
        self.linear_direction = 0
        self.rotation_direction = 0
        
        if self.key_handler[key.UP]:
            self.linear_direction += 1

        if self.key_handler[key.DOWN]:
            self.linear_direction -= 1
        
        if self.key_handler[key.LEFT]:
            self.rotation_direction -= 1

        if self.key_handler[key.RIGHT]:
            self.rotation_direction += 1

        
        # Modification des pins des roues
        [w.stop() for w in self.wheels]
        if self.rotation_direction == 0:
            if self.linear_direction > 0:
                [w.forward() for w in self.wheels]
            elif self.linear_direction < 0:
                [w.backward() for w in self.wheels]
                
        elif self.rotation_direction > 0:
            self.wheels[0].forward()
            self.wheels[2].forward()
            self.wheels[1].backward()
            self.wheels[3].backward()
                
        elif self.rotation_direction < 0:
            self.wheels[0].backward()
            self.wheels[2].backward()
            self.wheels[1].forward()
            self.wheels[3].forward()
        
        
        # Calcul du mouvement par rapport aux valeurs des roues :
        # Chaque roue apporte une force vers l'avant ou l'arrière par
        # rapport à la valeur de ses pins, plus une rotation horaire ou
        # anti-horaire.
        #
        # Ex.: roue 1 (devant-gauche), si sa direction va vers l'avant
        # (p1 = 1, p2 = 0), elle apporte une force vers l'avant et une
        # rotation horaire.
        linear_speed = 0
        rotation_speed = 0
        for w in self.wheels:
            # Calcul vitesse linéaire
            linear_speed += w.get_linear_speed()
            
            # Calcul vitesse de rotation
            rotation_speed += w.get_rotation_speed()
        
        
        # Actualisation de la position par rapport aux vitesses
        
        # Rotation de l'objet
        self.rotation += rotation_speed * dt
        
        # Avancement de l'objet
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * linear_speed * dt
        force_y = math.sin(angle_radians) * linear_speed * dt
        self.velocity_x = self.velocity_coeff * force_x
        self.velocity_y = self.velocity_coeff * force_y
        
        
        # Actualisation de l'information du robot
        self.set_robot_gpio()
        
        super(Player, self).update(dt)


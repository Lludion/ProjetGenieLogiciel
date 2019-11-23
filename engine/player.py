import sys
import os
import numpy as np
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)

from controlableNode import ControlableNode
from solidPlatform import SolidPlatform
from controller import KeyboardController
from hitbox import Hitbox
from rect import Rect
from vector import Vector
from force import Jump

class Player(ControlableNode):
    """ Player Class """
    def __init__(self):
        ControlableNode.__init__(self)
        self.set_hit_box(Hitbox(Rect(-1,-2,12,16)))
        self.set_rigid_body(True)
        self.create_sps("player")
        self.set_state("r")
        #self.set_sps(None)
        #self.get_sps().load_automaton()
        #self.get_sps().load_sprites()
        self.controller = PlayerController(self)
        self.score = 0
        self.alive = True
        
        self.jump_strength = 10
        self.can_jump = True
        self.is_jumping = False

    def start_jump(self):
        """ Key has just been pressed """
        speed = self.get_speed()
        #print(self.can_jump, not self.is_jumping, speed.y >= 0)
        if self.can_jump and (not self.is_jumping) and speed.y >= 0:
            self.set_speed(Vector(speed.x, -self.jump_strength))
            self.can_jump = False
            print("SET J")
            self.set_state("j") #For the spriteScheduler -> state jump (j)

    def stop_jump(self):
        """ Key has just been released """
        speed = self.get_speed()
        self.set_speed(Vector(speed.x,0))
        self.is_jumping = False

    def allow_jump(self):
        """ Allow the player to jump """
        self.can_jump = True

    def collide(self,o,sides,o2_sides):
        """ Player collides with o """
        if isinstance(o,SolidPlatform):
            if o2_sides == [0]:

                #if self.alive:
                if self.can_jump:
                    self.set_state("r") #For the spriteScheduler -> state run (r)
                #Top side
                self.allow_jump()
                self.is_jumping = False

                
            else:
                #The player dies
                self.die()

    def die(self):
        """ Kills the player """
        #self.set_state("d") #For the spriteScheduler -> state die (d)
        print("Player Dies")
        self.alive = False
            
    def add_score(self,val):
        self.score += val

    def get_score(self):
        return self.score

class PlayerController(KeyboardController):
    """ Controller for the player """
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed):
        """ Execute controller code """
        jump_key = pygame.K_z
        if pressed[jump_key]:
            self.target.start_jump()
        if event is not None and event.type == pygame.KEYUP:
            if event.key == jump_key:
                self.target.stop_jump()
        self.target.can_jump = False #Pour qu'on ne puisse pas sauter dans les airs

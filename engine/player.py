
import numpy as np
import pygame
from collections import defaultdict


from engine.jumpableNode import JumpableNode,JumpableController
from engine.solidPlatform import SolidPlatform
from engine.hitbox import Hitbox
from engine.rect import Rect
from engine.vector import Vector
from engine.projectile import Projectile
import engine.mobs.mob

""" The player object -> represents the player controllableNode """

class Player(JumpableNode):
    """ Player Class """
    def __init__(self):
        super().__init__()
        self.set_hit_box(Hitbox(Rect(-1,-2,12,16))) #Specific Hit box
        self.set_rigid_body(True) #it's a rigid body

        self.create_sps("player") #Set sprite
        self.animation_speed = 0.05
        self.set_state("r") #First state : runing ('r')
        self.controller = PlayerController(self) #Controller for the player (see below)
        self.score = 0 #Score of the player

        self.small = False #Life bar

        self.inventory = defaultdict(int) #Ref to inventory to give items to Campaign mod

        self.score_to_add = 0 #Score to add for animations

    def __repr__(self):
        return "Player("+str(self.get_hit_box())+")"

    def copy(self):
        raise NotImplementedError

    def paste_in(self,p):
        raise NotImplementedError

    def end_init(self):
        """ Used at the end of the creation of the GameLevel """
        self.add_force(self.world.gravity)

    def load_inventory(self,inv):
        """ Load the inventory of campaign mod """
        self.inventory = inv

    def set_inventory(self,items):#Should be renamed to add_inventory
        """ Add in inventory the aforementiened items"""
        for item in items:
            if item.type != "key":#item.type == "csm": #For consommable (may have several)
                self.inventory[item] += items[item]
            else:
                self.inventory[item] = items[item]

    def get_inventory(self):
        return self.inventory


    def collide(self,o,side,o2_side):
        """ Player collides with o """
        super().collide(o,side,o2_side)
        if isinstance(o,engine.mobs.mob.Mob):
            if o.alive:
                self.take_damages(o.damages)

        if isinstance(o,Projectile) and o.lifecollide:
            self.take_damages(o.damages)

    def die(self):
        """ Kills the player """
        self.set_state("d") #For the spriteScheduler -> state die (d)
        super().die()

    def update(self,dt):
        """ Update var, such as score, poison timeout, score """
        if self.poisoned_timeout == 10:
            self.add_score(-999)

        super().update(dt)

        if self.score_to_add > 0:
            valadd = min(50,self.score_to_add)
            valprod = int(self.score_to_add/10+0.5)
            val = max(valadd,valprod)
            self.score += val
            self.score_to_add -= val


        if self.score_to_add < 0:
            valadd = max(-50,self.score_to_add) #this is <0
            valprod = int(self.score_to_add/10+0.5)
            val = min(valadd,valprod)
            self.score += val
            self.score_to_add -= val


    def flush_score(self):
        """ Score is added entirely at the end of a level """
        self.score += self.score_to_add
        self.score_to_add = 0

    def add_score(self,val):
        """ New score will be added in a cool way """
        self.score_to_add += val

    def get_score(self):
        """ Returns the score """
        return self.score

class PlayerController(JumpableController):
    """ Controller for the player """
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        """ Execute controller code """
        jump_key = pygame.K_z
        if (event is not None and event.type == pygame.KEYDOWN and event.key == jump_key) or pressed[jump_key]:
            self.target.start_jump()
        if event is not None and event.type == pygame.KEYUP:
            if event.key == jump_key:
                self.target.stop_jump()
        super().execute(event,pressed,dt)

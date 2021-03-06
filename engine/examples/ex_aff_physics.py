import sys
import os
import numpy as np
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)
from polygone import *
from vector import Vector
from transform import Transform
from solidPlatform import SolidPlatform
import gameLevel
from rect import Rect
from force import Gravity
from hypothesis import given
from hypothesis.strategies import integers, lists

from hitbox import Hitbox

pygame.init()
fen = pygame.display.set_mode((500, 500),0)

#Coordinates for the platform
x = 0
y = 10

#Let's start by creating the polygon for hit_boxes

p = Rect(-1,-1,2,2) #Creates the polygon corresponding to the given sequence -> it's a rectangle
hb = Hitbox(p)
#Now let's build the platform associated to this polygon and move it to our coordinates
plat = SolidPlatform(hb)
plat.set_sps(None)
plat.translate(Vector(x,y))


#To create an other platform with the same hit box it easy:
plat2 = plat.copy()
plat3 = plat.copy()
plat4 = plat.copy()
plat2.translate(Vector(0.5,-5))
plat3.translate(Vector(0.1,-5))
plat4.translate(Vector(0.3,-15))



"""
hb3 = hb.copy()
plat3 = SolidPlatform(hb3)
plat3.set_sps(None)
plat3.translate(Vector(10.5,1))

hb4 = hb.copy()
plat4 = SolidPlatform(hb4)
plat4.set_sps(None)
plat4.translate(Vector(9,10))
"""
gravity = Gravity(5)

#plat2.rotate(np.pi/5)
#plat2.add_force(gravity)
#plat.add_force(gravity)
plat2.add_force(gravity)
plat3.add_force(gravity)
plat4.add_force(gravity)

def pos(t):
    return 0

gl = gameLevel.GameLevel([plat,plat2],pos)
gl.load_camera(fen) #Load the camera in the window fen
gl.get_camera().set_dimension(Vector(20,20)) #Resize the camera
gl.get_camera().set_position(Vector(-5,-5))
gl.aff(1/30)
for i in range(200):
    print("p2",plat2.get_position(),plat2.get_speed())
    gl.aff(1/30)
    gl.physics_step(1/30)
    #pygame.time.wait(50)

pygame.time.wait(500)

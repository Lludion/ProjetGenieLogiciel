from controlableNode import ControlableNode
from spriteScheduler import *
from hitbox import Hitbox
from rect import Rect
from player import Player
from items import KeyItem

""" Key class to show interactions between game and campaign"""

class Key(ControlableNode):
    def __init__(self,hb,name='empty'):
        ControlableNode.__init__(self)
        self.set_hit_box(hb)
        self.set_collide(True)
        self.create_sps("key")
        print("--",self.get_sps().ata)
        self.center_hit_box()

        self.taken = False

    def center_hit_box(self):
        self.get_hit_box().center()

    def copy(self):
        """ Returns the copy of this """
        sd = SolidPlatform(Hitbox(Rect(0,0,0,0)))
        self.paste_in(sd)
        return sd

    def paste_in(self,t):
        ControlableNode.paste_in(self,t)

    def collide(self,o2,side,other_side):
        #side : 0-> haut (aiguilles d'une montre)
        if isinstance(o2,Player):
            if not(self.taken):
                o2.set_inventory({KeyItem("key_1"):1})
                print("INV",id(o2.get_inventory()))
                self.taken = True
                self.create_sps('empty')
                self.set_state('a')
                
    


from imports import *
from tools import PseudoRd

class Level_2_fantasy(Level):
    
    def __init__(self,g):
        super().__init__(g)
        
    def fun_dialogue(self,g,arg):
        if arg == "start":
            if self.get_finished():
                quit_all = g.dict_dial["dial_odd2b"].show(g)
            else:
                quit_all = g.dict_dial["dial_odd2b"].show(g)
        elif arg == "bad_end":
            quit_all = g.dict_dial["dial_odd2abad"].show(g)
        elif arg == "good_end":
            quit_all = g.dict_dial["dial_odd2a"].show(g)
        return quit_all
            
    def reward(self,g):
        g.player.set_inventory({KeyItem("elvish_poem") : 1})
        
    def check_victory(self,g,arg):
        return arg
        
    def launch(self,g):
        print("FANTASY\n")
        quit_all = self.fun_dialogue(g,"start")
        self.objects = self.create_objects(g)
        self.set_accessed()
        print("-",self.objects)
        
        if quit_all:
            return False
        
        def player_pos(t):
            return t*100

        gl = GameLevel(self.objects,player_pos,name="level_2_fantasy",parallax=g.options["parallax"])
        gl.load_inventory(g.player.get_inventory())
        
        #g.launch_music(text) #too soon, create gap between music and level
        
        success = self.check_victory(g, g.launch_level(gl,None))
        pygame.event.get()#to capture inputs made during the wait
        
        if success:
            self.fun_dialogue(g,"good_end")
            if not self.get_finished():
                self.reward(g)
            self.set_finished()
        else:
            self.fun_dialogue(g,"bad_end")
        
        return success
    
    def create_objects(self,g):
        plats = []
        length = 85
        height = 18
        ln = 100
        y = -5
        plats = [SolidPlatform(Hitbox(Rect(-10,y,length,height)),sps="platform")]
        rd = PseudoRd(27,3,1024,74)
        for i in range(1,45):
            x = i*ln-10
            y = rd.get(y-20,y+20)
            if i == 15:
                plat = SolidPlatform(Hitbox(Rect(x,y,length-10,height)),sps="platform")
                plats.append(plat)
                plat = SolidPlatform(Hitbox(Rect(x+length-10,y+200,length+200,height)),sps="platform")
                plats.append(plat)
                flag = Flag(Hitbox(Rect(x+length+200-10,y+200-20,10,20)))
                plats.append(flag)
                y -= 40
                continue
            plat = SolidPlatform(Hitbox(Rect(x,y,length-rd(-10,10),height)),sps="platform")
            plats.append(plat)
            if rd(0,50) == 0:
                deadly = DeadlyPotion(Hitbox(Rect(x+rd.get(0,length),y-10,10,10)))
                plats.append(deadly)

            if rd(0,3) == 0:
                coin = Coin(Hitbox(Rect(x+rd(0,length),y-10-rd(0,70),10,10)))
                plats.append(coin)

        
        
        return plats

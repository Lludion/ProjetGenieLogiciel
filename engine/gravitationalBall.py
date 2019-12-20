from projectile import Projectile
from laserBallShield import LaserBallShield

class GravitationalBall(Projectile):
    def __init__(self,world):
        super().__init__()
        self.damages = 1
        self.create_sps("spike")
        self.link_world(world)
        self.solidcollide = False
        self.speed = 5

    def copy(self):
        gb = GravitationalBall(self.world)
        self.paste_in(gb)
        return gb

    def paste_in(self,gb):
        gb.load()

    def load(self):
        s = LaserBallShield()
        s.size = 10
        s.nb = 5
        self.add_shield(s)

    def collide(self,o,side,oside):
        super().collide(o,side,oside)

class GravitationalBallController:
    def __init__(self,target=None):
        super().__init__()
        self.target = target

    def execute(self,event,pressed,dt):
        self.move(dt)

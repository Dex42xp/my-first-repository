import pygame as pg
import numba as nb
import numpy as np


class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)
        
class PointLight:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        
class Camera:
    def __init__(self,position):
        self.position = position


class Application():
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.FPS = 500
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.running = True
        
    def draw(self):
        self.screen.fill((0,0,0))
        #pg.surfarray.blit_array(self.screen, )
        
    def run(self):
        self.running = True
        while self.running:
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            
if __name__ == "__main__":
    app = Application()
    app.run()
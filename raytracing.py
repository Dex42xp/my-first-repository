import pygame as pg
import numba as nb
import numpy as np

#class Object():

class Rasterization():
    def __init__(self, app):
        self.app = app

class RayTracing():
    def __init__(self, app):
        self.app = app
        print(self.screen_array)

class App():
    def __init__(self, res=(1600,900)):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = res
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH//2, self.HEIGHT//2
        self.FPS = 500
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.running = True
        
    def run(self):
        self.running = True
        while self.running:
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.screen.fill((0,0,0))
            pg.display.set_caption("FPS: " + str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            
            
if __name__ == "__main__":
    app = App()
    rasterization = Rasterization(app)
    rayTracing = RayTracing(app)
    app.run()

import pygame as pg
import numpy as np

def norm(vec):
    return vec / np.linalg.norm(vec)

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []

    def add_obj(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

class PointLight:
    def __init__(self, pos, color):
        self.position = np.array(pos)
        self.color = np.array(color)

class Sphere:
    def __init__(self, pos, rad, color):
        self.pos = np.array(pos)
        self.rad = rad
        self.color = np.array(color)
    
    def intersect(self, ro, rd):
        oc = ro - self.pos
        a = np.dot(rd, rd)
        b = 2 * np.dot(oc, rd)
        c = np.dot(oc, oc) - self.rad ** 2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None
        sqrt_disc = np.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
        elif t1 > 0:
            return t1
        elif t2 > 0:
            return t2
        return None

class Camera:
    def __init__(self, pos, look_at, fov, aspect_ratio):
        self.pos = np.array(pos, dtype=np.float64)
        self.look_at = np.array(look_at, dtype=np.float64)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.height = 2 * np.tan(np.deg2rad(self.fov) / 2)
        self.width = self.height * self.aspect_ratio

        self.update()
        
    def update(self):
        self.forward = norm(self.look_at - self.pos)
        self.right = norm(np.cross([0, 0, 1], self.forward))
        self.up = np.cross(self.forward, self.right)
        

def trace_ray(scene, ro, rd):
    closest_t = float('inf')
    closest_obj = None
    
    for obj in scene.objects:
        t = obj.intersect(ro, rd)
        if t is not None and t < closest_t and t > 0:
            closest_t = t
            closest_obj = obj

    if closest_obj is None:
        return np.array([127, 199, 255])
    return closest_obj.color

def rt_render(cam, scene, res):
    cw, ch = res
    canvas = np.zeros((cw, ch, 3), dtype=np.uint8)
    print(len(canvas), len(canvas[0]), len(canvas[0][0]))
    for i in range(cw):
        for j in range(ch):
            u = (j + 0.5) / cw
            v = (i + 0.5) / ch
            rd = cam.forward + (u - 0.5) * cam.width * cam.up + (v - 0.5) * cam.height * cam.right
            rd = norm(rd)
            color = trace_ray(scene, cam.pos, rd)
            canvas[i, j] = np.clip(color, 0, 255)
    return canvas

class Application:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 150, 100  # Увеличенное разрешение
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES, pg.SCALED)
        self.clock = pg.time.Clock()
        self.running = True
        
        self.move_speed = 0.2
        self.rotate_speed = 0.1
        self.camera1 = Camera([0, 0, 0], [1, 0, 0], 60, self.WIDTH / self.HEIGHT)
        self.scene1 = Scene()
        self.scene1.add_obj(Sphere([3, 0, -1], 0.7, [255, 0, 0]))  # Красная сфера
        self.scene1.add_obj(Sphere([4, 2, 0], 1.4, [0, 0, 255]))   # Синяя сфера
        self.scene1.add_obj(Sphere([4, -2, 0], 1, [0, 255, 0]))  # Зелёная сфера
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        canvas = rt_render(self.camera1, self.scene1, self.RES)
        pg.surfarray.blit_array(self.screen, canvas)
        
    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.running = False
            
            # Перемещение
            if keys[pg.K_w]:
                self.camera1.pos += self.camera1.forward * self.move_speed
                self.camera1.look_at += self.camera1.forward * self.move_speed
            if keys[pg.K_s]:
                self.camera1.pos -= self.camera1.forward * self.move_speed
                self.camera1.look_at -= self.camera1.forward * self.move_speed
            if keys[pg.K_a]:
                self.camera1.pos -= self.camera1.right * self.move_speed
                self.camera1.look_at -= self.camera1.right * self.move_speed
            if keys[pg.K_d]:
                self.camera1.pos += self.camera1.right * self.move_speed
                self.camera1.look_at += self.camera1.right * self.move_speed
            if keys[pg.K_e]:
                self.camera1.pos += self.camera1.up * self.move_speed
                self.camera1.look_at += self.camera1.up * self.move_speed
            if keys[pg.K_q]:
                self.camera1.pos -= self.camera1.up * self.move_speed
                self.camera1.look_at -= self.camera1.up * self.move_speed
            
            # Поворот
            direction = self.camera1.look_at - self.camera1.pos
            if keys[pg.K_LEFT]:
                # Поворот влево вокруг оси Z (yaw)
                direction_new = direction * np.cos(self.rotate_speed) - np.cross([0, 0, 1], direction) * np.sin(self.rotate_speed)
                self.camera1.look_at = self.camera1.pos + direction_new
                self.camera1.update()
            if keys[pg.K_RIGHT]:
                # Поворот вправо вокруг оси Z (yaw)
                direction_new = direction * np.cos(-self.rotate_speed) - np.cross([0, 0, 1], direction) * np.sin(-self.rotate_speed)
                self.camera1.look_at = self.camera1.pos + direction_new
                self.camera1.update()
            if keys[pg.K_UP]:
                # Поворот вверх вокруг оси Y (pitch)
                direction_new = direction * np.cos(self.rotate_speed) + np.cross(self.camera1.right, direction) * np.sin(-self.rotate_speed)
                self.camera1.look_at = self.camera1.pos + direction_new
                self.camera1.update()
            if keys[pg.K_DOWN]:
                # Поворот вниз вокруг оси Y (pitch)
                direction_new = direction * np.cos(-self.rotate_speed) + np.cross(self.camera1.right, direction) * np.sin(self.rotate_speed)
                self.camera1.look_at = self.camera1.pos + direction_new
                self.camera1.update()
            
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            
if __name__ == "__main__":
    app = Application()
    app.run()
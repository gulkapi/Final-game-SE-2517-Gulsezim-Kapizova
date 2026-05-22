import pygame
from utils import Entity, Animator
from settings import load_sheet


class Enemy(Entity):
    """
    The base enemy. Patrolling the segment, animating.
    Subclasses ARE REQUIRED to redefine draw() — this is polymorphism.
    """
    def __init__(self, x, y, w, h, points=100):
        super().__init__(x, y, w, h)
        self.vx = -1.5
        self.points = points
        self.patrol_min = x - 120
        self.patrol_max = x + 40
        self.anim = None


    def update(self, *args) -> None:
        self.rect.x += self.vx
        if self.rect.x <= self.patrol_min or \
           self.rect.right >= self.patrol_max:
            self.vx *= -1
        
        if self.anim:
            self.anim.update()

    def draw(self, surface, cam_x) -> None:
        raise NotImplementedError ("The subclass must implement draw()")
    

class Motobug(Enemy):
    """
    A fast bug on wheels. 100 points.
    Inherits: Enemy → Entity
    Redefines: draw() ← polymorphism

    """
    def __init__(self, x, y):
        super().__init__(x, y, 40, 32, points=100)
        sheet = load_sheet ("motobug.png")
        self.anim = Animator (sheet, frames=4, w=40, h=32, speed=6, scale=(40,32))

    def draw(self, surface: pygame.Surface, cam_x: float) ->None:
        sx = int(self.rect.x - cam_x)
        sy = int(self.rect.y)
        frame = self.anim.get_frame()

        if self.vx > 0:
            frame = pygame.transform.flip (frame, True, False)
        surface.blit(frame, (sx, sy))


class Crabmeat(Enemy):
    """
    Slow crab with claws. 200 points.
    Inherits: Enemy → Entity
    Redefines: draw() ← polymorphism

    """
    def __init__(self, x, y):
        super().__init__(x, y, 44, 36, points=200)
        self.vx = -0.8
        sheet     = load_sheet("crabmeat.png")
        self.anim = Animator(sheet, frames=6, w=44, h=36,
                             speed=8, scale=(44, 36))
 
    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        sx    = int(self.rect.x - cam_x)
        sy    = int(self.rect.y)
        frame = self.anim.get_frame()
        if self.vx > 0:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (sx, sy))
 


 

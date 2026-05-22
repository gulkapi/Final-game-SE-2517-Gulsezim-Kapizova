import pygame
from utils import Entity, Animator
from settings import load_sheet


class Fireball(Entity):
    """
    The Blaze shell. It flies horizontally,
    destroys enemies when touched.
    Inherits: Entity
    """

    SPEED = 8

    def __init__(self, x: float, y: float, direction: int):

        super().__init__(x, y, 24, 24)
        self.direction = direction
        self.vx = self.SPEED * direction


        sheet = load_sheet("fireball.png")
        self.anim = Animator(sheet, frames=6, w=24, h=24, speed=3, scale=(24,24))

    def update(self, *args) -> None:
        self.rect.x += self.vx
        self.anim.update()


        if self.rect.x > 3000 or self.rect.x < -100:
            self.alive = False

    
    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        if not self.alive:
            return
        sx = int(self.rect.x - cam_x)
        sy = int(self.rect.y)
        frame = self.anim.get_frame()
        if self.direction == -1:
            frame = pygame.transform.flip(frame,True,False)
        surface.blit(frame, (sx, sy))
import pygame
import math
from utils import Entity, Animator
from enemy import Motobug, Crabmeat
from settings import load_img, load_sheet, GOLD


#  PLATFORM
class Platform(Entity):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image = load_img("platform.png", scale=(int(w), int(h)))

    def update(self, *args): pass

    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        sx = int(self.rect.x - cam_x)
        surface.blit(self.image, (sx, int(self.rect.y)))


#  RING
class Ring(Entity):

    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        sheet     = load_sheet("rings.png")
        self.anim = Animator(sheet, frames=8, w=16, h=16,
                             speed=4, scale=(16, 16))

    def update(self, *args) -> None:
        self.anim.update()

    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        sx = int(self.rect.x - cam_x)
        sy = int(self.rect.y)
        surface.blit(self.anim.get_frame(), (sx, sy))


#  SOL EMERALD
class SolEmerald(Entity):
    """
    Sol Emerald is the target of the level.
    Glow animation + wobble.
    sol_emerald.png — 6 frames, each 40x40
    
    """

    POINTS = 200

    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        sheet          = load_sheet("sol_emerald.png")
        self.anim      = Animator(sheet, frames=6, w=40, h=40,
                                  speed=7, scale=(40, 40))
        self.bob       = 0.0
        self.collected = False

    def update(self, *args) -> None:
        self.anim.update()
        self.bob += 0.05

    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        if self.collected:
            return
        sx = int(self.rect.x - cam_x)
        sy = int(self.rect.y + math.sin(self.bob) * 5)
        surface.blit(self.anim.get_frame(), (sx, sy))


#  LEVEL
class Level:
    """
    Contains all the objects of the level:
    platforms, rings, enemies, Sol Emerald.

    """

    def __init__(self):
        self.platforms = []
        self.rings     = []
        self.enemies   = []
        self.emerald   = None
        self.completed = False
        self._build()

    def _build(self) -> None:
        P = Platform

        # surface
        self.platforms.append(P(-200, 440, 2600, 60))

        # platforms
        tiles = [
            (150, 350, 120, 20), (340, 290, 100, 20),
            (500, 330, 130, 20), (680, 270, 110, 20),
            (850, 350, 100, 20), (1000, 300, 120, 20),
            (1160, 240, 100, 20),(1300, 310, 130, 20),
            (1480, 270, 100, 20),(1640, 330, 120, 20),
            (1800, 280, 100, 20),(1950, 350, 120, 20),
        ]
        self.platforms += [P(*t) for t in tiles]

        # rings
        for x in range(160, 260, 20):
            self.rings.append(Ring(x, 410))
        for x in (360, 380, 400):
            self.rings.append(Ring(x, 260))
        for x in (510, 530, 550, 570):
            self.rings.append(Ring(x, 300))
        for x in (700, 720, 740):
            self.rings.append(Ring(x, 240))
        for x in (860, 880, 900):
            self.rings.append(Ring(x, 320))
        for x in (1020, 1040, 1060):
            self.rings.append(Ring(x, 270))
        for x in (1170, 1190, 1210):
            self.rings.append(Ring(x, 210))

        # enemies
        self.enemies = [
            Motobug(300,  408), Motobug(600,   408),
            Motobug(900,  408), Motobug(1200,  408),
            Crabmeat(500, 300), Crabmeat(800,  300),
            Crabmeat(1100,268), Crabmeat(1500, 238),
            Motobug(1700, 408), Crabmeat(1900, 248),
        ]

        self.emerald = SolEmerald(2050, 395)

    def update(self) -> None:
        for ring in self.rings:
            ring.update()
        for e in self.enemies:
            if e.alive:
                e.update()
        if self.emerald:
            self.emerald.update()

    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        for p in self.platforms:
            p.draw(surface, cam_x)
        for r in self.rings:
            r.draw(surface, cam_x)
        for e in self.enemies:
            if e.alive:
                e.draw(surface, cam_x)
        if self.emerald and not self.emerald.collected:
            self.emerald.draw(surface, cam_x)
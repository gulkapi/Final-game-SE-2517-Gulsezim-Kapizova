import pygame
from utils import Entity,  Animator
from settings import (GRAVITY, PLAYER_SPEED, JUMP_POWER, load_sheet)
from fireball import Fireball


class Player(Entity):
    """
    The main character is Blaze.
    Inherits: Entity
    Can: run, jump, shoot fireballs,
           Collect rings, lose lives.
    """

    SHOOT_COOLDOWN = 25

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 48, 48)

        self.anim = {
            "run":   Animator(load_sheet("blaze_run.png"),
                              frames=8, w=48, h=48,
                              speed=5, scale=(48, 48)),
            "jump":  Animator(load_sheet("blaze_jump.png"),
                              frames=4, w=48, h=48,
                              speed=6, scale=(48, 48)),
            "shoot": Animator(load_sheet("blaze_shoot.png"),
                              frames=3, w=48, h=48,
                              speed=4, scale=(48, 48)),
        }
        self.current_anim = "run"


        self.on_ground = False
        self.rings = 0
        self.lives = 3
        self.score = 0
        self.invincible = 0
        self.facing = 1
        self.cooldown = 0
        self.shoot_timer = 0
        self.fireballs = []


    def update(self, keys, platforms) -> None:
        self._handle_input(keys)
        self._apply_gravity()
        self._move_and_collide(platforms)
        self._tick_timers()
        self._update_fireballs(platforms)
        self._pick_animation()
        self.anim[self.current_anim].update()

    def _handle_input(self, keys) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.facing = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.facing = 1
        else:
            self.vx *= 0.7

        
        #jump
        jump_keys = (pygame.K_UP, pygame.K_w, pygame.K_SPACE)
        if any(keys[k] for k in jump_keys) and self.on_ground:
            self.vy        = JUMP_POWER
            self.on_ground = False
        
        #shoot Z or F
        if (keys[pygame.K_z] or keys[pygame.K_f]) and self.cooldown ==0:
            self._shoot()

    def _shoot(self) ->None:
        fx = self.rect.centerx + (24 * self.facing)
        fy = self.rect.centery - 4
        self.fireballs.append(Fireball(fx, fy, self.facing))
        self.cooldown = self.SHOOT_COOLDOWN
        self.shoot_timer = 12

    #physics
    def _apply_gravity(self) ->None:
        self.vy = min(self.vy + GRAVITY, 18)


    def _move_and_collide(self, platforms) ->None:
        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                elif self.vx < 0:
                    self.rect.left = p.rect.right
                self.vx = 0

    #vertical
        self.on_ground = False
        self.rect.y += self.vy
        for p in platforms:
            if self.rect.colliderect (p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.rect.bottom
                self.vy = 0

    
    #game logic
    def hit_by_enemy(self) -> bool:
        if self.invincible > 0:
            return False
        if self.rings > 0:
            self.rings = 0
            self.invincible = 90
            return False
        self.lives -= 1
        self.invincible = 120
        return self.lives <= 0
    

    #timers and fireballs
    def _tick_timers(self) -> None:
        if self.invincible > 0: self.invincible -= 1
        if self.cooldown > 0: self.cooldown -= 1
        if self.shoot_timer > 0: self.shoot_timer -= 1
    
    def _update_fireballs(self, platforms) -> None:
        for fb in self.fireballs:
            fb.update()
        self.fireballs = [fb for fb in self.fireballs if fb.alive]


    #animation
    def _pick_animation(self) -> None:
        if self.shoot_timer > 0:
            new = "shoot"
        elif not self.on_ground:
            new = "jump"
        else:
            new = "run"

        if new != self.current_anim:
            self.anim[new].reset()
            self.current_anim = new

    
    #rendering
    def draw(self, surface: pygame.Surface, cam_x: float) ->None:
        if self.invincible > 0 and (self.invincible // 4) % 2 ==0:
            return
        
        sx = int(self.rect.x - cam_x)
        sy = int(self.rect.y)
        frame = self.anim[self.current_anim].get_frame()

        if self.facing == -1:
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, (sx, sy))

        for fb in self.fireballs:
            fb.draw(surface, cam_x)
            


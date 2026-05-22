import pygame 
import os

#Screen

SCREEN_W = 800
SCREEN_H = 480
FPS = 60
TITLE = "BlazeDash"

#Physics
GRAVITY = 0.55
PLAYER_SPEED = 5
JUMP_POWER = -13

#Colors (R,G,B)
WHITE = (255, 255, 255)
BLACK  = (0, 0, 0)
BLUE = (21, 101, 255)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
PURPLE  = (155,  48, 255)
SKY1 = (1, 6, 15)
SKY2 = (10, 32, 72)
GRAY    = (150, 150, 150)

#Paths
HIGHSCORE_FILE = "data/highscores.json"
IMAGES_DIR     = os.path.join("assets", "images")

def load_img(filename, scale=None):
    
    path = os.path.join(IMAGES_DIR, filename)
    try:
        img = pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        img = pygame.Surface((32, 32), pygame.SRCALPHA)
        img.fill((255, 0, 255, 180))  
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

def load_sheet(filename):
    path = os.path.join(IMAGES_DIR, filename)
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        surf = pygame.Surface((128, 32), pygame.SRCALPHA)
        surf.fill((255, 0, 255, 180))
        return surf
 
import os
import pygame
from settings import IMAGES_DIR

pygame.init()

print("Current working directory:", os.getcwd())
print("Looking for sprites in:", os.path.abspath(IMAGES_DIR))
print()

files = [
    "blaze_run.png",
    "blaze_jump.png", 
    "blaze_shoot.png",
    "motobug.png",
    "crabmeat.png",
    "fireball.png",
    "ring.png",
    "sol_emerald.png",
    "background.png",
    "platform.png"
]

for f in files:
    full_path = os.path.join(IMAGES_DIR, f)
    if os.path.exists(full_path):
        img = pygame.image.load(full_path)
        print(f"✓ {f}: {img.get_width()}x{img.get_height()}")
    else:
        print(f"✗ {f}: Not found in {full_path}")

print()
print("Does the assets folder exist?", os.path.exists("assets"))
print("Does the assets/images folder exist?", os.path.exists("assets/images"))
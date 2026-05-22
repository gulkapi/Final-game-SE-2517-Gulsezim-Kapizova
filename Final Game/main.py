import pygame
from settings import SCREEN_H, SCREEN_W, TITLE
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)
    game = Game(screen)
    game.run()
    pygame.quit()
 
 
if __name__ == "__main__":
    main()
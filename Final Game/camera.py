from settings import SCREEN_W

class Camera:
    WORLD_W = 2200
    LERP = 0.1
    
    def __init__(self):
        self.x = 0.0

    def follow(self, player) ->None:
        target = player.rect.centerx - SCREEN_W //3
        self.x += (target - self.x) * self.LERP
        self.x = max (0.0, min(self.WORLD_W - SCREEN_W, self.x))
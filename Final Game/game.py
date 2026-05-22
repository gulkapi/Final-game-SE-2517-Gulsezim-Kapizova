import pygame
from settings import (SCREEN_W, SCREEN_H, FPS,
                      SKY1, WHITE, GOLD, RED, PURPLE, GRAY,
                      load_img)
from player import Player
from level  import Level, SolEmerald
from camera import Camera
from score_manager import ScoreManager
from utils  import GameTimer


class Game:
    """
    The main controller of the game.
    States: "start" | "play" | "gameover" | "victory"
    """

    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.clock   = pygame.time.Clock()

        # fonts
        self.font_xl = pygame.font.SysFont("Arial", 52, bold=True)
        self.font_lg = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_md = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_sm = pygame.font.SysFont("Arial", 20)

        # the system
        self.scores  = ScoreManager()

        # background
        self.bg = load_img("background.png", scale=(SCREEN_W, SCREEN_H))

        # game objects 
        self.player     = None
        self.level      = None
        self.camera     = None
        self.timer      = None
        self.final_time = None

        self.state = "start"

    #  Transitions between states
    def start_game(self) -> None:
        self.player     = Player(60, 370)
        self.level      = Level()
        self.camera     = Camera()
        self.timer      = GameTimer()
        self.final_time = None
        self.state      = "play"

    def _trigger_game_over(self) -> None:
        self.timer.stop()
        self.final_time = self.timer.formatted()
        self.scores.save("BLAZE", self.player.score)
        self.state = "gameover"

    def _trigger_victory(self) -> None:
        self.timer.stop()
        self.final_time = self.timer.formatted()
        self.scores.save("BLAZE", self.player.score)
        self.state = "victory"


    #  THE MAIN CYCLE

    def run(self) -> None:
        while True:
            self.clock.tick(FPS)
            keys   = pygame.key.get_pressed()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    return
                self._handle_event(event)

            self._update(keys)
            self._draw()
            pygame.display.flip()

    #  EVENT HANDLING
    def _handle_event(self, event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.state in ("start", "gameover", "victory"):
                self.start_game()


    #  UPDATE 

    def _update(self, keys) -> None:
        if self.state != "play":
            return

        p = self.player

        p.update(keys, self.level.platforms)
        self.camera.follow(p)

        self.level.update()

        for ring in self.level.rings[:]:
            if p.intersects(ring):
                self.level.rings.remove(ring)
                p.rings  += 1
                p.score  += 10

        for e in self.level.enemies:
            if not e.alive:
                continue

            if p.intersects(e):
                stomp = (p.vy > 0 and
                         p.rect.bottom - p.vy <= e.rect.top + 10)
                if stomp:
                    e.alive  = False
                    p.score += e.points
                    p.vy     = -9   
                else:
                    if p.hit_by_enemy():
                        self._trigger_game_over()
                        return

        for fb in p.fireballs:
            if not fb.alive:
                continue
            for e in self.level.enemies:
                if not e.alive:
                    continue
                if fb.rect.colliderect(e.rect):
                    e.alive  = False
                    fb.alive = False
                    p.score += e.points
                    break

        em = self.level.emerald
        if em and not em.collected and p.intersects(em):
            em.collected    = True
            p.score        += SolEmerald.POINTS
            self.level.completed = True
            self._trigger_victory()
            return

        if p.rect.top > SCREEN_H + 80:
            if p.hit_by_enemy():
                self._trigger_game_over()
            else:
                p.rect.x = max(0, self.camera.x)
                p.rect.y = 370
                p.vx = p.vy = 0

    #  DRAW 
    def _draw(self) -> None:
        self.screen.fill(SKY1)

        if   self.state == "start":    self._draw_start()
        elif self.state == "play":     self._draw_play()
        elif self.state == "gameover": self._draw_gameover()
        elif self.state == "victory":  self._draw_victory()

    #  game screen
    def _draw_play(self) -> None:
        self.screen.blit(self.bg, (0, 0))

        cam = self.camera.x
        self.level.draw(self.screen, cam)
        self.player.draw(self.screen, cam)
        self._draw_hud()

    def _draw_hud(self) -> None:
        p      = self.player
        labels = [
            (f"SCORE  {p.score}",         (16,  10)),
            (f"RINGS  {p.rings}",          (210, 10)),
            (f"LIVES  {p.lives}",          (400, 10)),
            (f"BEST   {self.scores.get_high()}", (590, 10)),
            (f"TIME  {self.timer.formatted()}",  (16,  34)),
        ]
        for text, pos in labels:
            surf = self.font_sm.render(text, True, GOLD)
            self.screen.blit(surf, pos)

    def _draw_start(self) -> None:
        self._draw_title("BLAZEDASH", PURPLE, 150)
        self._draw_subtitle("Play as Blaze — find Sol the Emerald!", WHITE, 215)
        self._draw_subtitle("Controls: ← → movement | ↑/W/SPACE jump | Z/F fire", GRAY, 248)
        self._draw_scores(300)
        self._draw_subtitle("Press ENTER to start", GOLD, 430)

    def _draw_gameover(self) -> None:
        self._draw_title("GAME OVER", RED, 130)

        score_txt = f"Score:  {self.player.score}"
        time_txt  = f"Time:  {self.final_time}"
        self._draw_subtitle(score_txt, WHITE,  210)
        self._draw_subtitle(time_txt,  (100, 220, 255), 245)

        self._draw_scores(300)
        self._draw_subtitle("Press ENTER to repeat", GOLD, 440)


    def _draw_victory(self) -> None:
        self._draw_title("THE LEVEL IS PASSED!", GOLD, 110)

        em_txt    = f"Sol The Emerald has been found  +{SolEmerald.POINTS} points"
        score_txt = f"Final score:  {self.player.score}"
        time_txt  = f"Transit time:  {self.final_time}"

        self._draw_subtitle(em_txt,    PURPLE,           175)
        self._draw_subtitle(score_txt, WHITE,            215)
        self._draw_subtitle(time_txt,  (100, 220, 255),  250)

        self._draw_scores(300)
        self._draw_subtitle("Press ENTER to play again", GOLD, 440)


    def _draw_title(self, text: str, color, y: int) -> None:
        surf = self.font_xl.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, y)))

    def _draw_subtitle(self, text: str, color, y: int) -> None:
        surf = self.font_sm.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, y)))

    def _draw_scores(self, top_y: int) -> None:
        header = self.font_md.render("— ТОП РЕКОРДЫ —", True, GOLD)
        self.screen.blit(header, header.get_rect(center=(SCREEN_W // 2, top_y)))

        for i, entry in enumerate(self.scores.get_top()):
            txt  = f"{i+1}.  {entry['name']}  —  {entry['score']}"
            surf = self.font_sm.render(txt, True, WHITE)
            self.screen.blit(surf, surf.get_rect(
                center=(SCREEN_W // 2, top_y + 32 + i * 26)))
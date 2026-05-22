import time
import pygame 

class Entity:
    def __init__(self, x: float, y: float, w: int, h: int):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.alive: bool = True

    @property 
    def cx(self): 
        return self.rect.centerx

    @property 
    def cy(self): 
        return self.rect.centery

    def intersects(self, other: "Entity") -> bool:
        return self.rect.colliderect(other.rect)
    
    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError
    
    def draw(self, surface: pygame.Surface, cam_x: float) -> None:
        raise NotImplementedError
    

class Animator:
    def __init__(self, sheet: pygame.Surface,
                 frames: int, w: int, h: int,
                 speed: int = 6, scale=None):
        self.speed = speed
        self.index = 0
        self.timer = 0
        self.frames = []
        
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        
        # Если это заглушка (розовый квадрат), создаём цветные кадры
        is_placeholder = (sheet_width == 128 and sheet_height == 32)
        
        if is_placeholder:
            print(f"Creating placeholder animation with {frames} frames, size {w}x{h}")
            # Создаём красивые цветные кадры для отладки
            colors = [(255, 100, 100), (255, 150, 100), (255, 200, 100),
                      (255, 255, 100), (200, 255, 100), (150, 255, 100),
                      (100, 255, 100), (100, 255, 150)]
            for i in range(frames):
                frame = pygame.Surface((w, h), pygame.SRCALPHA)
                color = colors[i % len(colors)]
                pygame.draw.rect(frame, color, (0, 0, w, h))
                pygame.draw.rect(frame, (255, 255, 255), (0, 0, w, h), 2)
                if scale:
                    frame = pygame.transform.scale(frame, scale)
                self.frames.append(frame)
        else:
            # Нормальная загрузка спрайтов
            for i in range(frames):
                rect_x = i * w
                if rect_x + w <= sheet_width and h <= sheet_height:
                    frame = sheet.subsurface(pygame.Rect(rect_x, 0, w, h))
                    if scale:
                        frame = pygame.transform.scale(frame, scale)
                    self.frames.append(frame)
                else:
                    # Если не хватает места, создаём заглушку
                    frame = pygame.Surface((w, h), pygame.SRCALPHA)
                    frame.fill((255, 0, 255))
                    if scale:
                        frame = pygame.transform.scale(frame, scale)
                    self.frames.append(frame)
    
    def update(self) -> None:
        self.timer += 1
        if self.timer >= self.speed:
            if self.frames:
                self.index = (self.index + 1) % len(self.frames)
            self.timer = 0
 
    def get_frame(self) -> pygame.Surface:
        return self.frames[self.index] if self.frames else None
 
    def reset(self) -> None:
        self.index = 0
        self.timer = 0
 

class GameTimer:
    def __init__(self):
        self._start = time.time()
        self._stopped_at = None
 
    def stop(self) -> None:
        if self._stopped_at is None:
            self._stopped_at = time.time()
 
    def get_seconds(self) -> float:
        if self._stopped_at:
            return self._stopped_at - self._start
        return time.time() - self._start
 
    def formatted(self) -> str:
        total = self.get_seconds()
        mins = int(total // 60)
        secs = int(total % 60)
        tenth = int((total % 1) * 10)
        return f"{mins:02d}:{secs:02d}.{tenth}"
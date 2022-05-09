from .config import PLAYER_COLOR, HIT_COLOR
import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.speed = 0.75
        self.size = 10
        self.color = PLAYER_COLOR
        self.cooldown = 0

    @property
    def rect(self):
        x, y = int(self.x), int(self.y)
        return pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    def update(self, pressed, map, lastMap):
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.color = PLAYER_COLOR
                self.pos = map.starts[lastMap].pos
            return
        
        if pressed[pygame.K_LEFT]:
            self.vx -= self.speed
        if pressed[pygame.K_RIGHT]:
            self.vx += self.speed
        if pressed[pygame.K_UP]:
            self.vy -= self.speed
        if pressed[pygame.K_DOWN]:
            self.vy += self.speed

        self.vx *= 0.7
        self.vy *= 0.7
        self.x += self.vx
        self.y += self.vy

        for rect in map.rects:
            if self.rect.colliderect(rect):
                self.color = HIT_COLOR
                self.cooldown = 60
                self.vx = 0
                self.vy = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

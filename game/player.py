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
        self.deaths = 0

    def save(self):
        data = {}
        data["x"] = int(self.x)
        data["y"] = int(self.y)
        data["deaths"] = self.deaths
        return data

    def load(self, data):
        self.x = data.get("x", 150)
        self.y = data.get("y", 150)
        self.deaths = data.get("deaths", 0)

    @property
    def rect(self):
        x, y = int(self.x), int(self.y)
        return pygame.Rect(
            x - self.size // 2, y - self.size // 2,
            self.size, self.size)

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

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.vx -= self.speed
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.vx += self.speed
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.vy -= self.speed
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.vy += self.speed

        self.vx *= 0.7
        self.vy *= 0.7
        self.x += self.vx
        self.y += self.vy

    def checkDeath(self, map):
        for rect in map.rects:
            if self.rect.colliderect(rect):
                if self.cooldown == 0:
                    self.color = HIT_COLOR
                    self.cooldown = 60
                    self.vx = 0
                    self.vy = 0
                    self.deaths += 1
                    map.triggers.trigger("onDeath")
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

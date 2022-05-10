from .config import PLAYER_COLOR, HIT_COLOR
from .maps import maps
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
                    map.triggers.trigger("onDeath")
                return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Map11:
    @classmethod
    def onTreasure(cls, mapnum):
        # Map 5: 5->6 becomes 5->7
        end = list(maps[5].ends.values())[1]
        end.number = 7

class Map14:
    counters = []
    num = 14

    @classmethod
    def switch(cls, num):
        cls.num = num
        # 15->14 becomes 15->26 (or vice versa)
        end = list(maps[15].ends.values())[0]
        end.number = num

        # 13->14 becomes 13->26 (or vice versa)
        end = list(maps[13].ends.values())[1]
        end.number = num

class Map18:
    enabled = True

    @classmethod
    def onEnter(cls, mapnum):
        if cls.enabled:
            Map14.counters.append("L")
            if (Map14.counters[-5:] == ["L", "R", "L", "R", "L"] and
                    Map14.num == 14 and
                    not maps[27].treasures[0].collected):
                Map14.switch(26)

class Map19:
    enabled = True

    @classmethod
    def onEnter(cls, mapnum):
        if cls.enabled:
            Map14.counters.append("R")
            if (Map14.counters[-5:] == ["R", "L", "R", "L", "R"] and
                    Map14.num == 14 and
                    not maps[27].treasures[0].collected):
                Map14.switch(26)

class Map20:
    @classmethod
    def onEnter(cls, mapnum):
        # Map 5: 5->7 becomes 5->6
        if not maps[11].treasures[0].collected:
            end = list(maps[5].ends.values())[1]
            end.number = 6

class Map21:
    deaths = 0
    activated = False
    barrier = maps[21].rects[-1]

    @classmethod
    def onDeath(cls, mapnum):
        if cls.activated:
            cls.deaths += 1

            if cls.deaths == 9:
                maps[21].rects.pop(-1)

class Map22:
    @classmethod
    def onExit(cls, mapnum):
        Map21.activated = True

class Map23:
    @classmethod
    def onExit(cls, mapnum):
        Map21.activated = True

class Map24:
    @classmethod
    def onTreasure(cls, mapnum):
        maps[21].rects.append(Map21.barrier)

class Map26:
    @classmethod
    def onLeave(cls, mapnum):
        if maps[27].treasures[0].collected:
            Map14.switch(14)

maps[11].triggers.add(Map11)
maps[18].triggers.add(Map18)
maps[19].triggers.add(Map19)
maps[20].triggers.add(Map20)
maps[21].triggers.add(Map21)
maps[22].triggers.add(Map22)
maps[23].triggers.add(Map23)
maps[24].triggers.add(Map24)

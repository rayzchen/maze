from .config import BG_COLOR, TEXT_COLOR, BORDER_COLOR, BORDERS
import pygame
import pygame.freetype
import os
import json
pygame.freetype.init()

font = pygame.freetype.SysFont("consolas", 15)

class Text:
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text

class StartPos:
    def __init__(self, number, x, y):
        self.number = number
        self.pos = (x, y)

class EndRect:
    def __init__(self, number, rect):
        self.number = number
        self.rect = rect

class Map:
    def __init__(self, rects, texts, color, starts, ends):
        self.rects = rects
        self.texts = texts
        self.color = color
        self.starts = starts
        self.ends = ends
        self.number = 0

    def draw(self, surface):
        surface.fill(BG_COLOR)
        for rect in self.rects:
            pygame.draw.rect(surface, self.color, rect)
            if BORDERS:
                pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        for text in self.texts:
            text_surface, _ = font.render(text.text)
            surface.blit(text_surface, text.rect.topleft)

    @staticmethod
    def from_file(path):
        rects = []
        texts = []
        color = ()
        starts = {}
        ends = {}
        with open(path) as f:
            content = f.read()
        for line in content.rstrip().split("\n"):
            if line.startswith("#"):
                continue
            parts = line.split(" ")
            if parts[0] == "RECT":
                rects.append(pygame.Rect(*map(int, parts[1:])))
            elif parts[0] == "COLOR":
                color = tuple(map(int, parts[1:]))
            elif parts[0] == "START":
                number = int(parts[1])
                starts[number] = StartPos(number, *map(int, parts[2:]))
            elif parts[0] == "END":
                number = int(parts[1])
                ends[number] = EndRect(number, pygame.Rect(*map(int, parts[2:])))
            elif parts[0] == "TEXT":
                rect = pygame.Rect(*map(int, parts[1:5]))
                text = json.loads(" ".join(parts[5:]))
                texts.append(Text(rect, text))

        return Map(rects, texts, color, starts, ends)

maps = {}
thisdir = os.path.dirname(os.path.abspath(__file__))
for file in os.listdir(os.path.join(thisdir, "maps")):
    if file.startswith("map"):
        num = int(file[3:-4])
        maps[num] = Map.from_file(os.path.join(thisdir, "maps", file))
        maps[num].number = num
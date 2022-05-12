from .config import (
    BG_COLOR, TREASURE_SIZE, TREASURE_COLOR, BORDER_COLOR, DEBUG)
from inspect import signature
import pygame
import pygame.freetype
import os
import json
# Init freetype module
pygame.freetype.init()

# game/ folder
thisdir = os.path.dirname(os.path.abspath(__file__))
# Use packaged font at 15 pt
font = pygame.freetype.Font(os.path.join(thisdir, "DejaVuSansMono.ttf"), 15)

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

class Treasure:
    def __init__(self, pos):
        # Blank rect then set size and pos
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.size = (TREASURE_SIZE, TREASURE_SIZE)
        self.rect.center = pos
        self.collected = False
        treasures.append(self)

# List of all treasures
treasures = []

class Triggers:
    def __init__(self, map):
        # Event handlers for entering, exiting, dying etc
        self.classes = []
        self.map = map

    def add(self, cls):
        self.classes.append(cls)

    def remove(self, cls):
        self.classes.remove(cls)

    def trigger(self, event):
        if DEBUG:
            print(f"Event triggered on map {self.map.number}: {event!r}")
        for cls in self.classes:
            if hasattr(cls, event):
                if DEBUG:
                    print(f"    Event triggered: {cls.__name__}.{event}")
                func = getattr(cls, event)
                sig = signature(func)
                if "mapnum" in sig.parameters:
                    func(self.map.number)
                else:
                    func()

class Map:
    def __init__(self, rects, texts, color, starts, ends, treasures):
        self.rects = rects
        self.texts = texts
        self.color = color
        self.starts = starts
        self.ends = ends
        self.treasures = treasures
        self.number = 0
        self.triggers = Triggers(self)

    def draw(self, surface):
        # Draw map to screen
        surface.fill(BG_COLOR)

        # Rect at bottom
        for rect in self.rects:
            pygame.draw.rect(surface, self.color, rect)
            if DEBUG:
                # Borders on rects
                pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Treasure above rect
        for treasure in self.treasures:
            if not treasure.collected:
                pygame.draw.rect(surface, TREASURE_COLOR, treasure.rect)

        # Text on top of everything
        for text in self.texts:
            text_surface, _ = font.render(text.text)
            surface.blit(text_surface, text.rect.topleft)

    @staticmethod
    def from_file(path):
        # Load map from file
        rects = []
        texts = []
        color = ()
        starts = {}
        ends = []
        treasures = []
        with open(path) as f:
            content = f.read()
        for line in content.rstrip().split("\n"):
            if line.startswith("#"):
                continue
            parts = line.split(" ")
            if parts[0] == "RECT":
                # Syntax: RECT left top width height
                rects.append(pygame.Rect(*map(int, parts[1:])))
            elif parts[0] == "COLOR":
                # Syntax: COLOR r g b
                color = tuple(map(int, parts[1:]))
            elif parts[0] == "START":
                # Syntax: START mapnum x y
                number = int(parts[1])
                starts[number] = StartPos(number, *map(int, parts[2:]))
            elif parts[0] == "END":
                # Syntax: END mapnum left top width height
                number = int(parts[1])
                ends.append(EndRect(number, pygame.Rect(*map(int, parts[2:]))))
            elif parts[0] == "TEXT":
                # Syntax: TEXT left top width height text
                rect = pygame.Rect(*map(int, parts[1:5]))
                # Use json to load string
                text = json.loads(" ".join(parts[5:]))
                texts.append(Text(rect, text))
            elif parts[0] == "TREASURE":
                # Syntax: TREASURE x y
                pos = tuple(map(int, parts[1:]))
                treasures.append(Treasure(pos))

        return Map(rects, texts, color, starts, ends, treasures)

# Load all maps in game/maps/
maps = {}
for file in os.listdir(os.path.join(thisdir, "maps")):
    if file.startswith("map"):
        num = int(file[3:-4])
        maps[num] = Map.from_file(os.path.join(thisdir, "maps", file))
        maps[num].number = num

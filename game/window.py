import os
import time
from .config import SCREEN_SIZE
from .maps import maps, treasures
from .player import Player
from .mechanics import addTriggers, EndGame
import pygame
import json
import atexit
pygame.init()
addTriggers()

class Window:
    def __init__(self):
        atexit.register(self.save)
        self.lastMap = 1
        self.map = 1
        self.player = Player()
        self.player.pos = maps[self.map].starts[self.lastMap].pos

        self.load()

        maps[self.map].triggers.trigger("onEnter")

        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    def draw(self):
        maps[self.map].draw(self.screen)
        self.player.draw(self.screen)

    def update(self):
        pygame.display.set_caption(str(self.map))

        pressed = pygame.key.get_pressed()
        self.player.update(pressed, maps[self.map], self.lastMap)
        dead = self.player.checkDeath(maps[self.map])

        if not dead:
            for end in maps[self.map].ends:
                if self.player.rect.colliderect(end.rect):
                    maps[self.map].triggers.trigger("onExit")
                    self.lastMap = self.map
                    self.map = end.number
                    self.player.pos = maps[self.map].starts[self.lastMap].pos
                    maps[self.map].triggers.trigger("onEnter")

            for treasure in maps[self.map].treasures:
                if not treasure.collected:
                    if self.player.rect.colliderect(treasure.rect):
                        treasure.collected = True
                        maps[self.map].triggers.trigger("onTreasure")

    def mainloop(self):
        done = False
        clock = pygame.time.Clock()
        while not done:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    done = True

            try:
                self.update()
            except EndGame:
                self.notify()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        pygame.display.quit()

    def notify(self):
        print("You won!")
        self.player.pos = (-10, -10)
        self.map = 39
        self.player.cooldown = -1

    def save(self):
        data = {}
        data["player"] = self.player.save()

        data["window"] = {}
        data["window"]["lastMap"] = self.lastMap
        data["window"]["map"] = self.map
        data["window"]["duration"] = time.time() - self.start
        if self.map == 39:
            data["window"]["disable"] = 1

        data["treasures"] = [t.collected for t in treasures]

        with open("save.txt", "w+") as f:
            f.write(json.dumps(data, indent=4))

    def load(self):
        if not os.path.isfile("save.txt"):
            self.start = time.time()
            return

        load = ""
        while load not in ["y", "n"]:
            load = input("Do you want to load savegame? (y/n) ").lower()
            if load not in ["y", "n"]:
                print("That is not a valid option!")
        if load == "n":
            self.start = time.time()
            return

        with open("save.txt") as f:
            data = json.loads(f.read())

        # Use get in case field doesn't exist
        window = data.get("window", {})
        self.player.load(data.get("player", {}))
        self.lastMap = window.get("lastMap", 1)
        self.map = window.get("map", 1)
        self.start = time.time() - window.get("duration")
        if "disable" in window:
            self.player.cooldown = -1

        sub = [False for _ in treasures]
        for i in range(len(treasures)):
            if data.get("treasures", sub)[i]:
                treasures[i].collected = True

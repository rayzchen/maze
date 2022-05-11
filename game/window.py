import os
from .config import SCREEN_SIZE
from .maps import maps
from .player import Player
from .mechanics import addTriggers
import pygame
import json
import atexit
pygame.init()
addTriggers()

class Window:
    def __init__(self):
        atexit.register(self.save)
        self.lastMap = 25
        self.map = 29
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

            self.draw()
            self.update()
            pygame.display.flip()
            clock.tick(60)
        pygame.display.quit()

    def save(self):
        data = {}
        data["player"] = self.player.save()
        with open("save.txt", "w+") as f:
            f.write(json.dumps(data))

    def load(self):
        if not os.path.isfile("save.txt"):
            return

        load = ""
        while load not in ["y", "n"]:
            load = input("Do you want to load savegame? (y/n) ").lower()
            if load not in ["y", "n"]:
                print("That is not a valid option!")
        if load == "n":
            return

        with open("save.txt") as f:
            data = json.loads(f.read())
        self.player.load(data["player"])

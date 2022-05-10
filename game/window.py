from .config import SCREEN_SIZE
from .maps import maps
from .mechanics import Player
import pygame
pygame.init()

class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.lastMap = 1
        self.map = 1
        self.player = Player()
        self.player.pos = maps[self.map].starts[self.lastMap].pos

    def draw(self):
        maps[self.map].draw(self.screen)
        self.player.draw(self.screen)

    def update(self):
        pygame.display.set_caption(str(self.map))

        pressed = pygame.key.get_pressed()
        self.player.update(pressed, maps[self.map], self.lastMap)
        dead = self.player.checkDeath(maps[self.map])

        if not dead:
            for end in maps[self.map].ends.values():
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

def main():
    window = Window()
    window.mainloop()

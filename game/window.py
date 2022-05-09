from .config import SCREEN_SIZE
from .maps import maps
from .mechanics import Player
import pygame
pygame.init()

class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.map = 3
        self.lastMap = 2
        self.player = Player()
        self.player.pos = maps[self.map].starts[self.lastMap].pos

    def draw(self):
        maps[self.map].draw(self.screen)
        self.player.draw(self.screen)

    def update(self):
        pressed = pygame.key.get_pressed()
        self.player.update(pressed, maps[self.map], self.lastMap)
        for end in maps[self.map].ends.values():
            if self.player.rect.colliderect(end.rect):
                self.lastMap = self.map
                self.map = end.number
                self.player.pos = maps[self.map].starts[self.lastMap].pos

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

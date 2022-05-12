from .maps import maps, treasures
from .config import DEBUG
import random

class EndGame(Exception):
    pass

class Map11:
    @classmethod
    def onTreasure(cls):
        # Close treasure 1
        # Map 5: 5->6 becomes 5->7
        maps[5].ends[1].number = 7

class Map14:
    counters = []
    num = 14

    @classmethod
    def switch(cls, num):
        if DEBUG:
            print(f"        Clue 2: change map {num}")

        # Open or close clue 2
        cls.num = num
        # 15->14 becomes 15->26 (or vice versa)
        maps[15].ends[0].number = num

        # 13->14 becomes 13->26 (or vice versa)
        maps[13].ends[1].number = num

class Map18:
    activated = False

    @classmethod
    def onEnter(cls):

        # Open clue 2
        if cls.activated:
            Map14.counters.append("L")
            if (Map14.counters[-5:] == ["L", "R", "L", "R", "L"] and
                    Map14.num == 14 and
                    not maps[27].treasures[0].collected):
                Map14.switch(26)
                if DEBUG:
                    print(f"        Clue 2: open")

class Map19:
    activated = False

    @classmethod
    def onEnter(cls):
        # Open clue 2
        if cls.activated:
            Map14.counters.append("R")
            if (Map14.counters[-5:] == ["R", "L", "R", "L", "R"] and
                    Map14.num == 14 and
                    not maps[27].treasures[0].collected):
                Map14.switch(26)
                if DEBUG:
                    print(f"        Clue 2: open")

class Map20:
    @classmethod
    def onEnter(cls):
        if DEBUG:
            print(f"        Clue 1: unlock")

        # Open clue 1
        # Map 5: 5->7 becomes 5->6
        if not maps[11].treasures[0].collected:
            maps[5].ends[1].number = 6

class Map21:
    deaths = 0
    activated = False
    barrier = maps[21].rects[-1]

    @classmethod
    def onDeath(cls):
        if DEBUG:
            print(f"        Clue 1: open")

        # Open clue 3
        if cls.activated:
            cls.deaths += 1

            if cls.deaths == 9:
                maps[21].rects.pop(-1)

class Map22:
    activated = False
    @classmethod
    def onExit(cls):
        # Activate clue 3
        if cls.activated:
            Map21.activated = True

class Map23:
    activated = False
    @classmethod
    def onExit(cls):
        # Activate clue 3
        if cls.activated:
            Map21.activated = True

class Map24:
    @classmethod
    def onTreasure(cls):
        if DEBUG:
            print(f"        Clue 3: close")

        # Close clue 3
        maps[21].rects.append(Map21.barrier)

class Map25:
    number = random.randint(0, 2)
    @classmethod
    def onEnter(cls):
        if DEBUG:
            print(f"        Tunnel: {cls.number}")

        # Random tunnel
        maps[25].ends[cls.number].number = 29

class Map26:
    @classmethod
    def onLeave(cls):
        if DEBUG:
            print(f"        Clue 2: close")

        # Close clue 2
        if maps[27].treasures[0].collected:
            Map14.switch(14)

class Map28:
    @classmethod
    def onEnter(cls):
        if DEBUG:
            print(f"        Clue 3: unlock")

        # Activate clue 3
        Map22.activated = True
        Map23.activated = True

class Map30:
    @classmethod
    def onEnter(cls):
        if DEBUG:
            print(f"        Clue 2: unlock")

        # Activate clue 2
        Map18.activated = True
        Map19.activated = True

class Map31:
    parts = maps[31].rects[:-2]
    @classmethod
    def onEnter(cls):
        # Final room

        number = 0
        for treasure in treasures:
            if treasure.collected:
                number += 1

        if DEBUG:
            print(f"        Final room: {number} treasures")

        if number == 4:
            maps[31].rects = maps[31].rects[:-2]

    @classmethod
    def onTreasure(cls):
        # Finish
        raise EndGame

class EnterCounter:
    maps = []
    @classmethod
    def onEnter(cls, mapnum):
        if mapnum not in cls.maps:
            cls.maps.append(mapnum)

class Map38:
    @classmethod
    def onEnter(cls):
        # Maps 32, 33, 34, 35, 36, 37
        if len(EnterCounter.maps) == 6:
            maps[38].rects.pop(-1)

def addTriggers():
    maps[11].triggers.add(Map11)
    maps[18].triggers.add(Map18)
    maps[19].triggers.add(Map19)
    maps[20].triggers.add(Map20)
    maps[21].triggers.add(Map21)
    maps[22].triggers.add(Map22)
    maps[23].triggers.add(Map23)
    maps[24].triggers.add(Map24)
    maps[25].triggers.add(Map25)
    maps[26].triggers.add(Map26)
    maps[28].triggers.add(Map28)
    maps[30].triggers.add(Map30)
    maps[31].triggers.add(Map31)
    maps[32].triggers.add(EnterCounter)
    maps[33].triggers.add(EnterCounter)
    maps[34].triggers.add(EnterCounter)
    maps[35].triggers.add(EnterCounter)
    maps[36].triggers.add(EnterCounter)
    maps[37].triggers.add(EnterCounter)
    maps[38].triggers.add(Map38)

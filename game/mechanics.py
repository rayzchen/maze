from .maps import maps
import random

class Map11:
    @classmethod
    def onTreasure(cls, mapnum):
        # Map 5: 5->6 becomes 5->7
        maps[5].ends[1].number = 7

class Map14:
    counters = []
    num = 14

    @classmethod
    def switch(cls, num):
        cls.num = num
        # 15->14 becomes 15->26 (or vice versa)
        maps[15].ends[0].number = num

        # 13->14 becomes 13->26 (or vice versa)
        maps[13].ends[1].number = num

class Map18:
    enabled = False

    @classmethod
    def onEnter(cls, mapnum):
        if cls.enabled:
            Map14.counters.append("L")
            if (Map14.counters[-5:] == ["L", "R", "L", "R", "L"] and
                    Map14.num == 14 and
                    not maps[27].treasures[0].collected):
                Map14.switch(26)

class Map19:
    enabled = False

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
            maps[5].ends[1].number = 6

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

class Map25:
    number = random.randint(0, 2)
    @classmethod
    def onEnter(cls, mapnum):
        print(cls.number)
        maps[25].ends[cls.number].number = 29

class Map26:
    @classmethod
    def onLeave(cls, mapnum):
        if maps[27].treasures[0].collected:
            Map14.switch(14)

class Map29:
    @classmethod
    def onEnter(cls, mapnum):
        Map18.enabled = True
        Map19.enabled = True

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
    maps[29].triggers.add(Map29)

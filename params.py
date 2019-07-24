class COLOR:
    GRAY = 0xAAAAAA
    RED = 0xFF7777
    BLUE = 0x7777FF
    GREEN = 0x77FF77

class RAID_DIFFICULTIES:
    LFR = 1
    FLEX = 2
    NORMAL = 3
    HEROIC = 4
    MYTHIC = 5

class GAME_ICON:
    MYTHIC_PLUS = "https://wow.zamimg.com/images/wow/icons/large/inv_relics_hourglass.jpg"

class REALM:
    _realms = dict()

    @classmethod
    def exists(cls, name):
        if name in cls._realms or name in cls._realms.values():
            return True
        return False

    @classmethod
    def KR(cls, arg):
        if arg in cls._realms:
            return arg
        for k, v in cls._realms.items():
            if v == arg:
                return k
        return None

    @classmethod
    def EN(cls, arg):
        if arg in cls._realms.values():
            return arg
        if arg in cls._realms:
            return cls._realms[arg]
        return None

class RACE:
    _races = dict()

    @classmethod
    def ID(cls, arg):
        if arg in _races:
            return arg
        for k, v in cls._races.items():
            if v == arg:
                return k
        return None

    @classmethod
    def KR(cls, arg):
        if arg in cls._races.values():
            return arg
        if arg in cls._races:
            return cls._races[arg]
        return None

class CLASS:
    _classes = dict()

    @classmethod
    def ID(cls, arg):
        if arg in _classes:
            return arg
        for k, v in cls._classes.items():
            if v == arg:
                return k
        return None

    @classmethod
    def KR(cls, arg):
        if arg in cls._classes.values():
            return arg
        if arg in cls._classes:
            return cls._classes[arg]
        return None

class DUNGEON:
    _dungeons = dict()

    @classmethod
    def KR(cls, arg):
        if arg in cls._dungeons.values():
            return arg
        if arg.lower() in cls._dungeons:
            return cls._dungeons[arg.lower()]
        return None

    @classmethod
    def EN(cls, arg):
        if arg.lower() in cls._dungeons:
            return arg
        for k, v in cls._dungeons.items():
            if v == arg:
                return k
        return None


REGION = "kr"
LOCALE = "ko"
MAX_LEVEL = 120
MYTHIC_PLUS_RESULTS = {
    0: "소진",
    1: "시간내클리어+1", 
    2: "시간내클리어+2",
    3: "시간내클리어+3",
}

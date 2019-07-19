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

class SERVER:
    _servers = {
        "아즈샤라": "Azshara",
        "듀로탄": "Durotan",
        "헬스크림": "Hellscream",
        "하이잘": "Hyjal",
        "알렉스트라자": "Alexstrasza",
        "데스윙": "Deathwing",
        "불타는군단": "Burning Legion",
        "스톰레이지": "Stormrage",
        "세나리우스": "Cenarius",
        "달라란": "Dalaran",
        "말퓨리온": "Malfurion",
        "노르간논": "Norgannon",
        "가로나": "Garona",
        "굴단": "Gul'dan",
        "줄진": "Zul'jin",
        "렉사르": "Rexxar",
        "와일드해머": "Wildhammer",
        "윈드러너": "Windrunner",
    }

    @classmethod
    def exists(cls, name):
        if name in cls._servers or name in cls._servers.values():
            return True
        return False

    @classmethod
    def KR(cls, arg):
        if arg in cls._servers:
            return arg
        for k, v in cls._servers.items():
            if v == arg:
                return k
        return None

    @classmethod
    def EN(cls, arg):
        if arg in cls._servers.values():
            return arg
        if arg in cls._servers:
            return cls._servers[arg]
        return None

class RACE:
    _races = {
        1: "인간",
        2: "오크",
        3: "드워프",
        4: "나이트엘프",
        5: "언데드",
        6: "타우렌",
        7: "노움",
        8: "트롤",
        9: "고블린",
        10: "블러드엘프",
        11: "드레나이",
        24: "판다렌",
        25: "판다렌",
        26: "판다렌",
        27: "나이트본",
        28: "높은산타우렌",
        29: "공허엘프",
        30: "빛벼림드레나이",
        31: "잔달라트롤",
        32: "쿨티란",
        34: "검은무쇠드워프",
        36: "마그하르오크",
    }

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
    _classes = {
        1: "전사",
        2: "성기사",
        3: "사냥꾼",
        4: "도적",
        5: "사제",
        6: "죽음의기사",
        7: "주술사",
        8: "마법사",
        9: "흑마법사",
        10: "수도사",
        11: "드루이드",
        12: "악마사냥꾼",
    }

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
    _dungeons = {
        "Siege of Boralus": "보랄러스 공성전",
        "Waycrest Manor": "웨이크레스트 저택",
        "The Underrot": "썩은굴",
        "Tol Dagor": "톨 다고르",
        "Freehold": "자유지대",
        "The MOTHERLODE!!": "왕노다지 광산!!",
        "Shrine of the Storm": "폭풍의 사원",
        "Atal'dazar": "아탈다자르",
        "Kings' Rest": "왕들의 안식처",
        "Temple of Sethraliss": "세스랄리스 사원",
    }

    @classmethod
    def KR(cls, arg):
        if arg in cls._dungeons.values():
            return arg
        if arg in cls._dungeons:
            return cls._dungeons[arg]
        return None

    @classmethod
    def EN(cls, arg):
        if arg in cls._dungeons:
            return arg
        for k, v in cls._dungeons.items():
            if v == arg:
                return k
        return None



REGION = "kr"
LOCALE = "ko"
MYTHIC_PLUS_RESULTS = {
    0: "소진",
    1: "시간내클리어+1", 
    2: "시간내클리어+2",
    3: "시간내클리어+3",
}

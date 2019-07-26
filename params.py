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
    MYTHIC_KEYSTONE = "inv_relics_hourglass"
    HORDE = "pvpcurrency-honor-horde"
    ALLIANCE = "pvpcurrency-honor-alliance"

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

class WCL_SPEC:
    def __init__(self, class_id, spec_id, name_en, icon, abbreviations):
        self.class_id = class_id
        self.spec_id = spec_id
        self.name_en = name_en
        self.icon = icon
        self.abbreviations = abbreviations

class WCL_CLASS:
    _classes = {
        "혈기 죽음의기사": WCL_SPEC(1, 1, "death_knight_blood",
            "spell_deathknight_bloodpresence", ["혈기", "혈죽", "죽탱"]),
        "냉기 죽음의기사": WCL_SPEC(1, 2, "death_knight_frost",
            "spell_deathknight_frostpresence", ["냉기", "냉죽"]),
        "부정 죽음의기사": WCL_SPEC(1, 3, "death_knight_unholy",
            "spell_deathknight_unholypresence", ["부정", "부죽"]),
        "조화 드루이드": WCL_SPEC(2, 1, "druid_balance",
            "spell_nature_starfall", ["조화", "조드"]),
        "야성 드루이드": WCL_SPEC(2, 2, "druid_feral",
            "ability_druid_catform", ["야성", "야드"]),
        "수호 드루이드": WCL_SPEC(2, 3, "druid_guardian",
            "ability_racial_bearform", ["수호", "수드", "야탱", "곰탱"]),
        "회복 드루이드": WCL_SPEC(2, 4, "druid_restoration",
            "spell_nature_healingtouch", ["회복", "회드"]),
        "야수 사냥꾼": WCL_SPEC(3, 1, "hunter_beast_mastery",
            "ability_hunter_bestialdiscipline", ["야수", "야냥"]),
        "사격 사냥꾼": WCL_SPEC(3, 2, "hunter_marksmanship",
            "ability_hunter_focusedaim", ["사격", "격냥"]),
        "생존 사냥꾼": WCL_SPEC(3, 3, "hunter_survival",
            "ability_hunter_camouflage", ["생존", "생냥"]),
        "비전 마법사": WCL_SPEC(4, 1, "mage_arcane",
            "spell_holy_magicalsentry", ["비전", "비법"]),
        "화염 마법사": WCL_SPEC(4, 2, "mage_fire",
            "spell_fire_firebolt02", ["화염", "화법"]),
        "냉기 마법사": WCL_SPEC(4, 3, "mage_frost",
            "spell_frost_frostbolt02", ["냉기", "냉법"]),
        "양조 수도사": WCL_SPEC(5, 1, "monk_brewmaster",
            "monk_stance_drunkenox", ["양조"]),
        "운무 수도사": WCL_SPEC(5, 2, "monk_mistweaver",
            "monk_stance_wiseserpent", ["운무"]),
        "풍운 수도사": WCL_SPEC(5, 3, "monk_windwalker",
            "monk_stance_whitetiger", ["풍운"]),
        "신성 성기사": WCL_SPEC(6, 1, "paladin_holy",
            "spell_holy_holybolt", ["신성", "신기"]),
        "보호 성기사": WCL_SPEC(6, 2, "paladin_protection",
            "ability_paladin_shieldofthetemplar", ["보호", "보기"]),
        "징벌 성기사": WCL_SPEC(6, 3, "paladin_retribution",
            "spell_holy_auraoflight", ["징벌", "징기"]),
        "수양 사제": WCL_SPEC(7, 1, "priest_discipline",
            "spell_holy_powerwordshield", ["수양", "수사"]),
        "신성 사제": WCL_SPEC(7, 2, "priest_holy",
            "spell_holy_guardianspirit", ["신성", "신사"]),
        "암흑 사제": WCL_SPEC(7, 3, "priest_shadow",
            "spell_shadow_shadowwordpain", ["암흑", "암사"]),
        "암살 도적": WCL_SPEC(8, 1, "rogue_assassination",
            "ability_rogue_eviscerate", ["암살"]),
        "잠행 도적": WCL_SPEC(8, 3, "rogue_subtlety",
            "ability_stealth", ["잠행"]),
        "무법 도적": WCL_SPEC(8, 4, "rogue_outlaw",
            "ability_backstab", ["무법"]),
        "정기 주술사": WCL_SPEC(9, 1, "shaman_elemental",
            "spell_nature_lightning", ["정기", "정술"]),
        "고양 주술사": WCL_SPEC(9, 2, "shaman_enhancement",
            "spell_nature_lightningshield", ["고양", "고술"]),
        "복원 주술사": WCL_SPEC(9, 3, "shaman_restoration",
            "spell_nature_magicimmunity", ["복원", "복술"]),
        "고통 흑마법사": WCL_SPEC(10, 1, "warlock_affliction",
            "spell_shadow_deathcoil", ["고통", "고흑"]),
        "악마 흑마법사": WCL_SPEC(10, 2, "warlock_demonology",
            "spell_shadow_metamorphosis", ["악마", "악흑"]),
        "파괴 흑마법사": WCL_SPEC(10, 3, "warlock_destruction",
            "spell_shadow_rainoffire", ["파괴", "파흑"]),
        "무기 전사": WCL_SPEC(11, 1, "warrior_arms",
            "ability_warrior_savageblow", ["무기", "무전"]),
        "분노 전사": WCL_SPEC(11, 2, "warrior_fury",
            "ability_warrior_innerrage", ["분노", "분전"]),
        "방어 전사": WCL_SPEC(11, 3, "warrior_protection",
            "ability_warrior_defensivestance", ["방어", "방전", "전탱"]),
        "파멸 악마사냥꾼": WCL_SPEC(12, 1, "demon_hunter_havoc",
            "ability_demonhunter_specdps", ["파멸", "악사", "악딜"]),
        "복수 악마사냥꾼": WCL_SPEC(12, 2, "demon_hunter_vengeance",
            "ability_demonhunter_spectank", ["복수", "악탱"]),
    }

    @classmethod
    def get(cls, name):
        if name in cls._classes:
            return cls._classes[name]
        return None

    @classmethod
    def get_by_abbreviation(cls, abbr):
        for i in cls._classes.values():
            if abbr in i.abbreviations:
                return i
        return None

def thumbnail(name):
    return "https://wow.zamimg.com/images/wow/icons/large/{}.jpg".format(name)


REGION = "kr"
LOCALE = "ko"
MAX_LEVEL = 120
MYTHIC_PLUS_RESULTS = {
    0: "소진",
    1: "시간내클리어+1", 
    2: "시간내클리어+2",
    3: "시간내클리어+3",
}
TALENTS_REQUIRED_LEVEL = [15, 30, 45, 60, 75, 90, 100]
SECONDARY_STAT = {
    32: "치명타 및 극대화",
    36: "가속",
    40: "유연성",
    49: "특화",
}

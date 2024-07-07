from enum import Enum

from rpgram.enums.emojis import EmojiEnum


class TargetEnum(Enum):
    SELF = 'self'
    SINGLE = 'single'
    TEAM = 'team'
    ALL = 'all'


class SkillTypeEnum(Enum):
    ATTACK = 'attack'
    BARRIER = 'barrier'
    BUFF = 'buff'
    DEFENSE = 'defense'
    HEALING = 'healing'


class SkillDefenseEnum(Enum):
    PHYSICAL = 'physical'
    MAGICAL = 'magical'
    TRUE = 'true'
    NA = 'n/a'


class TargetEmojiEnum(Enum):
    SELF = '🙋'
    SINGLE = '👤'
    TEAM = '👥'
    ALL = '🌐'


class SkillTypeEmojiEnum(Enum):
    ATTACK = EmojiEnum.ATTACK.value
    DEFENSE = EmojiEnum.DEFEND.value
    HEALING = EmojiEnum.HEALING.value
    BUFF = '🎖️'
    BARRIER = EmojiEnum.BARRIER_POINT.value


class SkillDefenseEmojiEnum(Enum):
    PHYSICAL = EmojiEnum.PHYSICAL_ATTACK.value
    MAGICAL = EmojiEnum.MAGICAL_ATTACK.value
    TRUE = '💯'
    NA = '⚫'


class BarbarianSkillEnum(Enum):
    FURIOUS_ATTACK = 'Ataque Furioso'
    WILD_STRIKE = 'Golpe Selvagem'
    WILD_RAM = 'Ariete Selvagem'
    FURIOUS_FURY = 'Fúria Furiosa'
    FURIOUS_INSTINCT = 'Instinto Furioso'
    FURIOUS_ROAR = 'Rugido Furioso'


class GuardianSkillEnum(Enum):
    ROBUST_BLOCK = 'Bloqueio Robusto'
    GUARDIAN_SHIELD = 'Escudo Guardião'
    SHIELD_WALL = 'Parede de Escudos'
    HEAVY_CHARGE = 'Investida Pesada'
    IRON_CHARGE = 'Investida de Ferro'
    STEEL_STORM = 'Tempestade de Aço'


class SorcererSkillEnum(Enum):
    MYSTICAL_PROTECTION = 'Proteção Mística'
    MYSTICAL_CONFLUENCE = 'Confluência Mística'
    MYSTICAL_VIGOR = 'Vigor Místico'
    PRISMATIC_SHOT = 'Disparo Prismático'
    PRISMATIC_SCINTILLATION = 'Cintilação Prismática'
    PRISMATIC_SHIELD = 'Escudo Prismático'
    CHAOS_ORB = 'Orbe do Caos'
    MAGICAL_VAMPIRISM = 'Vampirismo Mágico'
    SOUL_WEAVER = 'Tecelão de Almas'


class WarriorSkillEnum(Enum):
    POWERFUL_ATTACK = 'Ataque Poderoso'
    MORE_THAN_POWERFUL_ATTACK = 'Ataque Mais Que Poderoso'
    QUICK_ATTACK = 'Ataque Rápido'
    BLINK_ATTACK = 'Ataque Lampejante'
    LETHAL_ATTACK = 'Ataque Letal'
    AEGIS_SHADOW = 'Sombra de Égide'
    WAR_BANNER = 'Flâmula de Guerra'
    HEROIC_INSPIRATION = 'Inspiração Heroíca'
    WAR_CRY = 'Grito de Guerra'


TARGET_ENUM_NOT_SELF = [TargetEnum.SINGLE, TargetEnum.TEAM, TargetEnum.ALL]
MAGICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.MAGICAL]
PHYSICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.PHYSICAL, SkillDefenseEnum.TRUE]

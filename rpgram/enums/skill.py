from enum import Enum


class TargetEnum(Enum):
    SELF = 'self'
    SINGLE = 'single'
    TEAM = 'team'
    ALL = 'all'


class SkillTypeEnum(Enum):
    ATTACK = 'attack'
    DEFENSE = 'defense'
    HEALING = 'healing'


class SkillDefenseEnum(Enum):
    PHYSICAL = 'physical'
    MAGICAL = 'magical'
    TRUE = 'true'
    NA = 'n/a'


class BarbarianSkillEnum(Enum):
    FURIOUS_ATTACK = 'Ataque Furioso'
    WILD_STRIKE = 'Golpe Selvagem'
    FURIOUS_FURY = 'Fúria Furiosa'
    FURIOUS_INSTINCT = 'Instinto Furioso'


class GuardianSkillEnum(Enum):
    ROBUST_BLOCK = 'Bloqueio Robusto'
    HEAVY_CHARGE = 'Investida Pesada'


class SorcererSkillEnum(Enum):
    MYSTICAL_PROTECTION = 'Proteção Mística'
    MYSTICAL_CONFLUENCE = 'Confluência Mística'
    MYSTICAL_VIGOR = 'Vigor Místico'
    PRISMATIC_SHOT = 'Disparo Prismático'
    PRISMATIC_SCINTILLATION = 'Cintilação Prismática'


class WarriorSkillEnum(Enum):
    POWERFUL_ATTACK = 'Ataque Poderoso'
    MORE_THAN_POWERFUL_ATTACK = 'Ataque Mais Que Poderoso'
    QUICK_ATTACK = 'Ataque Rápido'
    LETHAL_ATTACK = 'Ataque Letal'


TARGET_ENUM_NOT_SELF = [TargetEnum.SINGLE, TargetEnum.TEAM, TargetEnum.ALL]
MAGICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.MAGICAL]
PHYSICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.PHYSICAL, SkillDefenseEnum.TRUE]

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


class GuardianSkillEnum(Enum):
    ROBUSTBLOCK = 'Bloqueio Robusto'
    HEAVYCHARGE = 'Investida Pesada'


TARGET_ENUM_NOT_SELF = [TargetEnum.SINGLE, TargetEnum.TEAM, TargetEnum.ALL]
MAGICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.MAGICAL]
PHYSICAL_DEFENSE_ENUM_LIST = [SkillDefenseEnum.PHYSICAL, SkillDefenseEnum.TRUE]

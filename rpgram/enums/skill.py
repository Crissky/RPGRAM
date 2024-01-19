from enum import Enum


class TargetEnum(Enum):
    SELF = 'self'
    SINGLE = 'single'
    TEAM = 'team'
    ALL = 'all'


class SkillTypeEnum(Enum):
    ATTACK = 'attack'
    DEFENSE = 'defense'

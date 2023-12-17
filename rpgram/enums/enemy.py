from enum import Enum


class EnemyStarsEnum(Enum):
    ONE = '⭐'
    TWO = '⭐⭐'
    THREE = '⭐⭐⭐'
    FOUR = '⭐⭐⭐⭐'
    FIVE = '🌟🌟🌟🌟🌟'
    BOSS = '👾'  # 👹👺


class AlignmentEnum(Enum):
    ASSASSIN = 'Assassino'
    BERSERK = 'Furioso'
    CAREGIVER = 'Cuidador'
    PROTECTOR = 'Protetor'

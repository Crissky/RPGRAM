from enum import Enum


class EnemyStarsEnum(Enum):
    ONE = '⭐'
    TWO = '⭐⭐'
    THREE = '⭐⭐⭐'
    FOUR = '⭐⭐⭐⭐'
    FIVE = '🌟🌟🌟🌟🌟'
    SUB_BOSS = '👺'
    BOSS = '👾'  # 👹


class AlignmentEnum(Enum):
    ASSASSIN = 'Assassino'
    BERSERK = 'Furioso'
    CAREGIVER = 'Cuidador'
    PROTECTOR = 'Protetor'
    SUPPORTER = 'Apoiador'

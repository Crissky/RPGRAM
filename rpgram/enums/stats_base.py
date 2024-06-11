from enum import Enum


class BaseStatsEnum(Enum):
    FOR = STRENGTH = 'FOR'
    DES = DEXTERITY = 'DES'
    CON = CONSTITUTION = 'CON'
    INT = INTELLIGENCE = 'INT'
    SAB = WISDOM = 'SAB'
    CAR = CHARISMA = 'CAR'
    XP = 'XP'
    LEVEL = 'LEVEL'
    CLASSE_LEVEL = 'CLASSE_LEVEL'


BASE_STATS_ATTRIBUTE_LIST = [
    BaseStatsEnum.LEVEL.value,
    BaseStatsEnum.CLASSE_LEVEL.value,
    BaseStatsEnum.XP.value,
    BaseStatsEnum.FOR.value,
    BaseStatsEnum.DES.value,
    BaseStatsEnum.CON.value,
    BaseStatsEnum.INT.value,
    BaseStatsEnum.SAB.value,
    BaseStatsEnum.CAR.value,
]

from enum import Enum


class CombatStatsEnum(Enum):
    HP = 'hp'
    CURRENT_HP = 'current_hp'
    INITIATIVE = 'initiative'
    PHYSICAL_ATTACK = 'physical_attack'
    PRECISION_ATTACK = 'precision_attack'
    MAGICAL_ATTACK = 'magical_attack'
    PHYSICAL_DEFENSE = 'physical_defense'
    MAGICAL_DEFENSE = 'magical_defense'
    HIT = 'hit'
    EVASION = 'evasion'


COMBAT_STATS_ATTRIBUTE_LIST = [
    CombatStatsEnum.HP.value,
    CombatStatsEnum.CURRENT_HP.value,
    CombatStatsEnum.INITIATIVE.value,
    CombatStatsEnum.PHYSICAL_ATTACK.value,
    CombatStatsEnum.PRECISION_ATTACK.value,
    CombatStatsEnum.MAGICAL_ATTACK.value,
    CombatStatsEnum.PHYSICAL_DEFENSE.value,
    CombatStatsEnum.MAGICAL_DEFENSE.value,
    CombatStatsEnum.HIT.value,
    CombatStatsEnum.EVASION.value,
]

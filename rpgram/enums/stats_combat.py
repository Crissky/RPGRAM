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

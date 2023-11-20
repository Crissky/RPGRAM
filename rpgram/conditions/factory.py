from rpgram.conditions import (
    Condition,
    BleedingCondition,
    BlindnessCondition,
    BurnCondition,
    ConfusionCondition,
    CurseCondition,
    ExhaustionCondition,
    FrozenCondition,
    ParalysisCondition,
    PetrifiedCondition,
    PoisoningCondition,
    SilenceCondition,
)
from rpgram.conditions.heal import (
    Heal1Condition,
    Heal2Condition,
    Heal3Condition,
    Heal4Condition,
    Heal5Condition,
    Heal6Condition,
    Heal7Condition,
    Heal8Condition,
)
from rpgram.enums.condition import (
    BLEEDING,
    BLINDNESS,
    BURN,
    CONFUSION,
    CURSE,
    EXHAUSTION,
    FROZEN,
    PARALYSIS,
    PETRIFIED,
    POISONING,
    SILENCE,
)
from rpgram.enums.consumable import HealingConsumableEnum


def factory_condition(condition_name, turn, level) -> Condition:
    # DEBUFFS
    if condition_name == BLEEDING:
        return BleedingCondition(turn, level)
    elif condition_name == BLINDNESS:
        return BlindnessCondition(turn, level)
    elif condition_name == BURN:
        return BurnCondition(turn, level)
    elif condition_name == CONFUSION:
        return ConfusionCondition(turn, level)
    elif condition_name == CURSE:
        return CurseCondition(turn, level)
    elif condition_name == EXHAUSTION:
        return ExhaustionCondition(turn, level)
    elif condition_name == FROZEN:
        return FrozenCondition(turn, level)
    elif condition_name == PARALYSIS:
        return ParalysisCondition(turn, level)
    elif condition_name == PETRIFIED:
        return PetrifiedCondition(turn, level)
    elif condition_name == POISONING:
        return PoisoningCondition(turn, level)
    elif condition_name == SILENCE:
        return SilenceCondition(turn, level)
    # HEALING BUFFS
    elif condition_name == HealingConsumableEnum.HEAL1.value:
        return Heal1Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL2.value:
        return Heal2Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL3.value:
        return Heal3Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL4.value:
        return Heal4Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL5.value:
        return Heal5Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL6.value:
        return Heal6Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL7.value:
        return Heal7Condition(turn, level)
    elif condition_name == HealingConsumableEnum.HEAL8.value:
        return Heal8Condition(turn, level)

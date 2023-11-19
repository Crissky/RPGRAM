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
from rpgram.enums.condition import ConditionEnum


def factory_condition(self, condition_name, turn, level) -> Condition:
    if condition_name == ConditionEnum.BLEEDING.name:
        return BleedingCondition(turn, level)
    elif condition_name == ConditionEnum.BLINDNESS.name:
        return BlindnessCondition(turn, level)
    elif condition_name == ConditionEnum.BURN.name:
        return BurnCondition(turn, level)
    elif condition_name == ConditionEnum.CONFUSION.name:
        return ConfusionCondition(turn, level)
    elif condition_name == ConditionEnum.CURSE.name:
        return CurseCondition(turn, level)
    elif condition_name == ConditionEnum.EXHAUSTION.name:
        return ExhaustionCondition(turn, level)
    elif condition_name == ConditionEnum.FROZEN.name:
        return FrozenCondition(turn, level)
    elif condition_name == ConditionEnum.PARALYSIS.name:
        return ParalysisCondition(turn, level)
    elif condition_name == ConditionEnum.PETRIFIED.name:
        return PetrifiedCondition(turn, level)
    elif condition_name == ConditionEnum.POISONING.name:
        return PoisoningCondition(turn, level)
    elif condition_name == ConditionEnum.SILENCE.name:
        return SilenceCondition(turn, level)

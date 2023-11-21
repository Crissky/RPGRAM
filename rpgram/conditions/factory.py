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


def factory_condition(
    condition_name: str,
    turn: int = None,
    level: int = None,
) -> Condition:
    # DEBUFFS
    if condition_name == BLEEDING:
        condition_class = BleedingCondition
    elif condition_name == BLINDNESS:
        condition_class = BlindnessCondition
    elif condition_name == BURN:
        condition_class = BurnCondition
    elif condition_name == CONFUSION:
        condition_class = ConfusionCondition
    elif condition_name == CURSE:
        condition_class = CurseCondition
    elif condition_name == EXHAUSTION:
        condition_class = ExhaustionCondition
    elif condition_name == FROZEN:
        condition_class = FrozenCondition
    elif condition_name == PARALYSIS:
        condition_class = ParalysisCondition
    elif condition_name == PETRIFIED:
        condition_class = PetrifiedCondition
    elif condition_name == POISONING:
        condition_class = PoisoningCondition
    elif condition_name == SILENCE:
        condition_class = SilenceCondition
    # HEALING BUFFS
    elif condition_name == HealingConsumableEnum.HEAL1.value:
        condition_class = Heal1Condition
    elif condition_name == HealingConsumableEnum.HEAL2.value:
        condition_class = Heal2Condition
    elif condition_name == HealingConsumableEnum.HEAL3.value:
        condition_class = Heal3Condition
    elif condition_name == HealingConsumableEnum.HEAL4.value:
        condition_class = Heal4Condition
    elif condition_name == HealingConsumableEnum.HEAL5.value:
        condition_class = Heal5Condition
    elif condition_name == HealingConsumableEnum.HEAL6.value:
        condition_class = Heal6Condition
    elif condition_name == HealingConsumableEnum.HEAL7.value:
        condition_class = Heal7Condition
    elif condition_name == HealingConsumableEnum.HEAL8.value:
        condition_class = Heal8Condition

    if turn and level:
        return condition_class(turn=turn, level=level)
    elif not turn and level:
        return condition_class(level=level)
    elif turn and not level:
        return condition_class(turn=turn)
    elif not turn and not level:
        return condition_class()

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
from rpgram.enums.debuff import (
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
    name: str = None,
    condition_name: str = None,
    turn: int = None,
    level: int = None,
) -> Condition:
    if isinstance(condition_name, str) and not isinstance(name, str):
        name = condition_name

    # DEBUFFS
    if name == BLEEDING:
        condition_class = BleedingCondition
    elif name == BLINDNESS:
        condition_class = BlindnessCondition
    elif name == BURN:
        condition_class = BurnCondition
    elif name == CONFUSION:
        condition_class = ConfusionCondition
    elif name == CURSE:
        condition_class = CurseCondition
    elif name == EXHAUSTION:
        condition_class = ExhaustionCondition
    elif name == FROZEN:
        condition_class = FrozenCondition
    elif name == PARALYSIS:
        condition_class = ParalysisCondition
    elif name == PETRIFIED:
        condition_class = PetrifiedCondition
    elif name == POISONING:
        condition_class = PoisoningCondition
    elif name == SILENCE:
        condition_class = SilenceCondition
    # HEALING BUFFS
    elif name == HealingConsumableEnum.HEAL1.value:
        condition_class = Heal1Condition
    elif name == HealingConsumableEnum.HEAL2.value:
        condition_class = Heal2Condition
    elif name == HealingConsumableEnum.HEAL3.value:
        condition_class = Heal3Condition
    elif name == HealingConsumableEnum.HEAL4.value:
        condition_class = Heal4Condition
    elif name == HealingConsumableEnum.HEAL5.value:
        condition_class = Heal5Condition
    elif name == HealingConsumableEnum.HEAL6.value:
        condition_class = Heal6Condition
    elif name == HealingConsumableEnum.HEAL7.value:
        condition_class = Heal7Condition
    elif name == HealingConsumableEnum.HEAL8.value:
        condition_class = Heal8Condition

    if turn and level:
        return condition_class(turn=turn, level=level)
    elif not turn and level:
        return condition_class(level=level)
    elif turn and not level:
        return condition_class(turn=turn)
    elif not turn and not level:
        return condition_class()

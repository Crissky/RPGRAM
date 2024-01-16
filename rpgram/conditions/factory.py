from rpgram.conditions.condition import Condition
from rpgram.conditions.debuff import (
    BerserkerCondition,
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
    StunnedCondition,
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
    BERSERKER,
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
    STUNNED,
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

    kwargs = {}
    if isinstance(turn, int):
        kwargs['turn'] = turn
    elif turn is not None:
        raise TypeError(f'Turno deve ser do tipo inteiro: {type(turn)}')

    if isinstance(level, int):
        kwargs['level'] = level
    elif level is not None:
        raise TypeError(f'Level deve ser do tipo inteiro: {type(level)}')

    # DEBUFFS
    if name == BERSERKER:
        condition_class = BerserkerCondition
    elif name == BLEEDING:
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
    elif name == STUNNED:
        condition_class = StunnedCondition
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

    return condition_class(**kwargs)


if __name__ == '__main__':
    print(factory_condition(name=CONFUSION))
    print(factory_condition(name=CONFUSION, turn=10))
    print(factory_condition(name=CONFUSION, level=10))
    print(factory_condition(name=CONFUSION, turn=10, level=10))

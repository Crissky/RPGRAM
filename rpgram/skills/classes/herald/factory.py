from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.herald.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    ColossalOnslaughtSkill,
    MysticBlockSkill,
    RobysticShieldSkill,
)
from rpgram.skills.classes.herald.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    FlameMantillaSkill,
    FlamesOfEquilibriumSkill,
    IgneousHeartSkill,
    IgneousStrikeSkill,
    PurifyingFlameSkill,
    VigilFlameSkill
)
from rpgram.skills.classes.multiclasse.physical_defense import (
    GuardianShieldSkill,
    HeavyChargeSkill,
    RobustBlockSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def herald_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == RobustBlockSkill.__name__:
        skill_class = RobustBlockSkill
    elif skill_class_name == MysticBlockSkill.__name__:
        skill_class = MysticBlockSkill
    elif skill_class_name == GuardianShieldSkill.__name__:
        skill_class = GuardianShieldSkill
    elif skill_class_name == RobysticShieldSkill.__name__:
        skill_class = RobysticShieldSkill
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    elif skill_class_name == ColossalOnslaughtSkill.__name__:
        skill_class = ColossalOnslaughtSkill
    # SKILL2
    elif skill_class_name == VigilFlameSkill.__name__:
        skill_class = VigilFlameSkill
    elif skill_class_name == FlameMantillaSkill.__name__:
        skill_class = FlameMantillaSkill
    elif skill_class_name == IgneousStrikeSkill.__name__:
        skill_class = IgneousStrikeSkill
    elif skill_class_name == PurifyingFlameSkill.__name__:
        skill_class = PurifyingFlameSkill
    elif skill_class_name == FlamesOfEquilibriumSkill.__name__:
        skill_class = FlamesOfEquilibriumSkill
    elif skill_class_name == IgneousHeartSkill.__name__:
        skill_class = IgneousHeartSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


HERALD_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RobustBlockSkill,
    MysticBlockSkill,
    GuardianShieldSkill,
    RobysticShieldSkill,
    HeavyChargeSkill,
    ColossalOnslaughtSkill,

    # SKILL2
    VigilFlameSkill,
    FlameMantillaSkill,
    IgneousStrikeSkill,
    PurifyingFlameSkill,
    FlamesOfEquilibriumSkill,
    IgneousHeartSkill,
]
HERALD_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2
]

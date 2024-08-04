from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.herald.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
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
    elif skill_class_name == GuardianShieldSkill.__name__:
        skill_class = GuardianShieldSkill
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


HERALD_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RobustBlockSkill,
    GuardianShieldSkill,
    HeavyChargeSkill,
]
HERALD_SKILL_WAYS: List[dict] = [
    skill_way1
]

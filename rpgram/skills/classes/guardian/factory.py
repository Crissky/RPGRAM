from typing import TYPE_CHECKING
from rpgram.skills.classes.guardian.skill1 import (
    GuardianShieldSkill,
    RobustBlockSkill
)
from rpgram.skills.classes.guardian.skill2 import (
    HeavyChargeSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def guardian_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == RobustBlockSkill.__name__:
        skill_class = RobustBlockSkill
    elif skill_class_name == GuardianShieldSkill.__name__:
        skill_class = GuardianShieldSkill
    # SKILL2
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


GUARDIAN_SKILL_LIST = [
    # SKILL1
    RobustBlockSkill,
    GuardianShieldSkill,

    # SKILL2
    HeavyChargeSkill,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.guardian.skill1 import (
    GuardianShieldSkill,
    RobustBlockSkill,
    ShieldWallSkill
)
from rpgram.skills.classes.guardian.skill2 import (
    HeavyChargeSkill,
    IronChargeSkill,
    SteelStormSkill
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
    elif skill_class_name == ShieldWallSkill.__name__:
        skill_class = ShieldWallSkill
    # SKILL2
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    elif skill_class_name == IronChargeSkill.__name__:
        skill_class = IronChargeSkill
    elif skill_class_name == SteelStormSkill.__name__:
        skill_class = SteelStormSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


GUARDIAN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RobustBlockSkill,
    GuardianShieldSkill,
    ShieldWallSkill,

    # SKILL2
    HeavyChargeSkill,
    IronChargeSkill,
    SteelStormSkill,
]

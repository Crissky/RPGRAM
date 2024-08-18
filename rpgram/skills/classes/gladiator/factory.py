from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.gladiator.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    AchillesAttackSkill,
    AjaxShieldSkill,
    ArenaDomainSkill,
    AresBladeSkill,
    HerculesFurySkill,
    TurtleStanceSkill,
    UnicornStanceSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def gladiator_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == AchillesAttackSkill.__name__:
        skill_class = AchillesAttackSkill
    elif skill_class_name == HerculesFurySkill.__name__:
        skill_class = HerculesFurySkill
    elif skill_class_name == AresBladeSkill.__name__:
        skill_class = AresBladeSkill
    elif skill_class_name == AjaxShieldSkill.__name__:
        skill_class = AjaxShieldSkill
    elif skill_class_name == TurtleStanceSkill.__name__:
        skill_class = TurtleStanceSkill
    elif skill_class_name == UnicornStanceSkill.__name__:
        skill_class = UnicornStanceSkill
    elif skill_class_name == ArenaDomainSkill.__name__:
        skill_class = ArenaDomainSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


GLADIATOR_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    AchillesAttackSkill,
    HerculesFurySkill,
    AresBladeSkill,
    AjaxShieldSkill,
    TurtleStanceSkill,
    UnicornStanceSkill,
    ArenaDomainSkill,
]
GLADIATOR_SKILL_WAYS: List[dict] = [
    skill_way1,
]

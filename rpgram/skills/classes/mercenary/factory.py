from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.mercenary.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    ImproviseSkill,
    NosebreakerSkill,
    SkullbreakerSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def mercenary_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == NosebreakerSkill.__name__:
        skill_class = NosebreakerSkill
    elif skill_class_name == SkullbreakerSkill.__name__:
        skill_class = SkullbreakerSkill
    elif skill_class_name == ImproviseSkill.__name__:
        skill_class = ImproviseSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


MERCENARY_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    NosebreakerSkill,
    SkullbreakerSkill,
    ImproviseSkill,
]
MERCENARY_SKILL_WAYS: List[dict] = [
    skill_way1,
]

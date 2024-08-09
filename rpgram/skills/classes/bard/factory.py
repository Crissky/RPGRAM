from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.bard.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DissonanceSkill,
    ResonanceSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def bard_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == DissonanceSkill.__name__:
        skill_class = DissonanceSkill
    elif skill_class_name == ResonanceSkill.__name__:
        skill_class = ResonanceSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BARD_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    DissonanceSkill,
    ResonanceSkill,
]
BARD_SKILL_WAYS: List[dict] = [
    skill_way1
]

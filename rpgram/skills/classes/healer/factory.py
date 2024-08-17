from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.healer.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    HealingTouchSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def healer_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == HealingTouchSkill.__name__:
        skill_class = HealingTouchSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


HEALER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    HealingTouchSkill,
]
HEALER_SKILL_WAYS: List[dict] = [
    skill_way1,
]

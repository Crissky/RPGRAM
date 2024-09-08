from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.samurai.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DoUchiSkill,
    KoteUchiSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def samurai_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == KoteUchiSkill.__name__:
        skill_class = KoteUchiSkill
    elif skill_class_name == DoUchiSkill.__name__:
        skill_class = DoUchiSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SAMURAI_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    KoteUchiSkill,
    DoUchiSkill,
]
SAMURAI_SKILL_WAYS: List[dict] = [
    skill_way1,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.rogue.skill1 import (
    VipersFangSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def rogue_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == VipersFangSkill.__name__:
        skill_class = VipersFangSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


ROGUE_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    VipersFangSkill,
]

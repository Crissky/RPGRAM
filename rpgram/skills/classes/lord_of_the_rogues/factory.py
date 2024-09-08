from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.multiclasse.precision_attack import QuickAttackSkill
from rpgram.skills.classes.lord_of_the_rogues.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DeadlyBladeSkill,
    SilentAssassinSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def lord_of_the_rogues_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == QuickAttackSkill.__name__:
        skill_class = QuickAttackSkill
    elif skill_class_name == SilentAssassinSkill.__name__:
        skill_class = SilentAssassinSkill
    elif skill_class_name == DeadlyBladeSkill.__name__:
        skill_class = DeadlyBladeSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


LORD_OF_THE_ROGUES_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    QuickAttackSkill,
    SilentAssassinSkill,
    DeadlyBladeSkill,
]
LORD_OF_THE_ROGUES_SKILL_WAYS: List[dict] = [
    skill_way1,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.duelist.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    SplashFountSkill,
    WindBladeSkill
)
from rpgram.skills.classes.multiclasse.precision_attack import QuickAttackSkill
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def duelist_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == QuickAttackSkill.__name__:
        skill_class = QuickAttackSkill
    elif skill_class_name == WindBladeSkill.__name__:
        skill_class = WindBladeSkill
    elif skill_class_name == SplashFountSkill.__name__:
        skill_class = SplashFountSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


DUELIST_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    QuickAttackSkill,
    WindBladeSkill,
    SplashFountSkill,
]
DUELIST_SKILL_WAYS: List[dict] = [
    skill_way1,
]

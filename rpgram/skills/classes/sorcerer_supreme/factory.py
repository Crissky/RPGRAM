from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.sorcerer_supreme.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    MagicOrbSkill,
    MagicShieldSkill,
    MagicShotSkill,
    MagicalImprisonmentSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def sorcerer_supreme_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == MagicOrbSkill.__name__:
        skill_class = MagicOrbSkill
    elif skill_class_name == MagicalImprisonmentSkill.__name__:
        skill_class = MagicalImprisonmentSkill
    elif skill_class_name == MagicShieldSkill.__name__:
        skill_class = MagicShieldSkill
    elif skill_class_name == MagicShotSkill.__name__:
        skill_class = MagicShotSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SORCERER_SUPREME_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    MagicOrbSkill,
    MagicalImprisonmentSkill,
    MagicShieldSkill,
    MagicShotSkill,
]
SORCERER_SUPREME_SKILL_WAYS: List[dict] = [
    skill_way1,
]

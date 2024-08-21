from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.summoner.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    FlamingSpecterSkill,
    KappaFountainSkill,
    PiskieWindbagSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def summoner_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == FlamingSpecterSkill.__name__:
        skill_class = FlamingSpecterSkill
    elif skill_class_name == KappaFountainSkill.__name__:
        skill_class = KappaFountainSkill
    elif skill_class_name == PiskieWindbagSkill.__name__:
        skill_class = PiskieWindbagSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SUMMONER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    FlamingSpecterSkill,
    KappaFountainSkill,
    PiskieWindbagSkill,
]
SUMMONER_SKILL_WAYS: List[dict] = [
    skill_way1,
]

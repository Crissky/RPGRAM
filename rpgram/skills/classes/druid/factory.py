from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.druid.skill1 import (
    GuardianBearSkill,
    HunterTigerSkill,
    RangerFalconSkill,
    WatcherOwlSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def druid_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == RangerFalconSkill.__name__:
        skill_class = RangerFalconSkill
    elif skill_class_name == GuardianBearSkill.__name__:
        skill_class = GuardianBearSkill
    elif skill_class_name == HunterTigerSkill.__name__:
        skill_class = HunterTigerSkill
    elif skill_class_name == WatcherOwlSkill.__name__:
        skill_class = WatcherOwlSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


DRUID_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RangerFalconSkill,
    GuardianBearSkill,
    HunterTigerSkill,
    WatcherOwlSkill,
]

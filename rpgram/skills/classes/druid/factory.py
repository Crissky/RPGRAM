from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.druid.skill1 import (
    GuardianBearSkill,
    HunterTigerSkill,
    RangerFalconSkill,
    WatcherOwlSkill
)
from rpgram.skills.classes.druid.skill2 import (
    OakArmorSkill,
    OakWarhammerSkill,
    SilkFlossSwordSkill,
    VineBucklerSkill,
    SilkFlossSpaulderSkill,
    VineWhipSkill
)
from rpgram.skills.classes.druid.skill3 import (
    PoisonousSapSkill
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
    # SKILL2
    elif skill_class_name == VineWhipSkill.__name__:
        skill_class = VineWhipSkill
    elif skill_class_name == SilkFlossSwordSkill.__name__:
        skill_class = SilkFlossSwordSkill
    elif skill_class_name == OakWarhammerSkill.__name__:
        skill_class = OakWarhammerSkill
    elif skill_class_name == VineBucklerSkill.__name__:
        skill_class = VineBucklerSkill
    elif skill_class_name == SilkFlossSpaulderSkill.__name__:
        skill_class = SilkFlossSpaulderSkill
    elif skill_class_name == OakArmorSkill.__name__:
        skill_class = OakArmorSkill
    # SKILL3
    elif skill_class_name == PoisonousSapSkill.__name__:
        skill_class = PoisonousSapSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


DRUID_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    RangerFalconSkill,
    GuardianBearSkill,
    HunterTigerSkill,
    WatcherOwlSkill,
    SilkFlossSwordSkill,
    OakWarhammerSkill,

    # SKILL2
    VineWhipSkill,
    VineBucklerSkill,
    SilkFlossSpaulderSkill,
    OakArmorSkill,

    # SKILL3
    PoisonousSapSkill,
]

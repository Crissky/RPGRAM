from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.mage.skill1 import (
    EarthBreakSkill,
    FireBallSkill,
    FulminantLightningSkill,
    IceShardSkill,
    MagicBlastSkill,
    RockArmorSkill,
    WaterBubbleSkill,
    WindGustSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def mage_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == FireBallSkill.__name__:
        skill_class = FireBallSkill
    elif skill_class_name == WaterBubbleSkill.__name__:
        skill_class = WaterBubbleSkill
    elif skill_class_name == WindGustSkill.__name__:
        skill_class = WindGustSkill
    elif skill_class_name == EarthBreakSkill.__name__:
        skill_class = EarthBreakSkill
    elif skill_class_name == MagicBlastSkill.__name__:
        skill_class = MagicBlastSkill
    elif skill_class_name == IceShardSkill.__name__:
        skill_class = IceShardSkill
    elif skill_class_name == FulminantLightningSkill.__name__:
        skill_class = FulminantLightningSkill
    elif skill_class_name == RockArmorSkill.__name__:
        skill_class = RockArmorSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


MAGE_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    FireBallSkill,
    WaterBubbleSkill,
    WindGustSkill,
    EarthBreakSkill,
    MagicBlastSkill,
    IceShardSkill,
    FulminantLightningSkill,
    RockArmorSkill,
]

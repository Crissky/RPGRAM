from typing import TYPE_CHECKING
from rpgram.skills.classes.warrior.skill1 import (
    MoreThanPowerfulAttackSkill,
    PowerfulAttackSkill
)
from rpgram.skills.classes.warrior.skill2 import (
    LethalAttackSkill,
    QuickAttackSkill
)
from rpgram.skills.classes.warrior.skill3 import (
    AegisShadowSkill,
    HeroicInspirationSkill,
    WarBannerSkill,
    WarCrySkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def warrior_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == PowerfulAttackSkill.__name__:
        skill_class = PowerfulAttackSkill
    elif skill_class_name == MoreThanPowerfulAttackSkill.__name__:
        skill_class = MoreThanPowerfulAttackSkill
    # SKILL2
    elif skill_class_name == QuickAttackSkill.__name__:
        skill_class = QuickAttackSkill
    elif skill_class_name == LethalAttackSkill.__name__:
        skill_class = LethalAttackSkill
    # SKILL3
    elif skill_class_name == AegisShadowSkill.__name__:
        skill_class = AegisShadowSkill
    elif skill_class_name == WarBannerSkill.__name__:
        skill_class = WarBannerSkill
    elif skill_class_name == HeroicInspirationSkill.__name__:
        skill_class = HeroicInspirationSkill
    elif skill_class_name == WarCrySkill.__name__:
        skill_class = WarCrySkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


WARRIOR_SKILL_LIST = [
    # SKILL1
    PowerfulAttackSkill,
    MoreThanPowerfulAttackSkill,

    # SKILL2
    QuickAttackSkill,
    LethalAttackSkill,

    # SKILL3
    AegisShadowSkill,
    WarBannerSkill,
    HeroicInspirationSkill,
    WarCrySkill,
]

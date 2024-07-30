from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.classes.warrior.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    MoreThanPowerfulAttackSkill,
    PowerfulAttackSkill
)
from rpgram.skills.classes.warrior.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    BlinkAttackSkill,
    LethalAttackSkill
)
from rpgram.skills.classes.warrior.skill3 import (
    SKILL_WAY_DESCRIPTION as skill_way3,
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
    elif skill_class_name == BlinkAttackSkill.__name__:
        skill_class = BlinkAttackSkill
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


WARRIOR_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    PowerfulAttackSkill,
    MoreThanPowerfulAttackSkill,

    # SKILL2
    QuickAttackSkill,
    BlinkAttackSkill,
    LethalAttackSkill,

    # SKILL3
    AegisShadowSkill,
    WarBannerSkill,
    HeroicInspirationSkill,
    WarCrySkill,
]
WARRIOR_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
    skill_way3,
]

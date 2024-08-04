from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.duelist.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    AgileFeetSkill,
    EagleEyeSkill,
    LungeSkill,
    SplashFountSkill,
    TranspassSkill,
    WindBladeSkill
)
from rpgram.skills.classes.duelist.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    AchillesHeelSkill,
    DirtyBlowSkill,
    DisarmorSkill,
    InverseSkill,
    SiegfriedsShoulderBladeSkill
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
    elif skill_class_name == AgileFeetSkill.__name__:
        skill_class = AgileFeetSkill
    elif skill_class_name == EagleEyeSkill.__name__:
        skill_class = EagleEyeSkill
    elif skill_class_name == LungeSkill.__name__:
        skill_class = LungeSkill
    elif skill_class_name == TranspassSkill.__name__:
        skill_class = TranspassSkill
    # SKILL2
    elif skill_class_name == InverseSkill.__name__:
        skill_class = InverseSkill
    elif skill_class_name == DirtyBlowSkill.__name__:
        skill_class = DirtyBlowSkill
    elif skill_class_name == AchillesHeelSkill.__name__:
        skill_class = AchillesHeelSkill
    elif skill_class_name == DisarmorSkill.__name__:
        skill_class = DisarmorSkill
    elif skill_class_name == SiegfriedsShoulderBladeSkill.__name__:
        skill_class = SiegfriedsShoulderBladeSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


DUELIST_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    QuickAttackSkill,
    WindBladeSkill,
    SplashFountSkill,
    AgileFeetSkill,
    EagleEyeSkill,
    LungeSkill,
    TranspassSkill,
    InverseSkill,
    DirtyBlowSkill,
    AchillesHeelSkill,
    DisarmorSkill,
    SiegfriedsShoulderBladeSkill,
]
DUELIST_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

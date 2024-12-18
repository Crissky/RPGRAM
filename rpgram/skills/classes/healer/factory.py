from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.healer.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    HealingHerbSkill,
    HealingTouchSkill,
    ReviveRitualSkill,
    VitalityAuraSkill,
)
from rpgram.skills.classes.healer.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    BeatifyingAegisSkill,
    HealingRefugeSkill,
    ProtectiveAuraSkill,
    ProtectiveInfusionSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def healer_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == HealingTouchSkill.__name__:
        skill_class = HealingTouchSkill
    elif skill_class_name == HealingHerbSkill.__name__:
        skill_class = HealingHerbSkill
    elif skill_class_name == VitalityAuraSkill.__name__:
        skill_class = VitalityAuraSkill
    elif skill_class_name == ReviveRitualSkill.__name__:
        skill_class = ReviveRitualSkill
    # SKILL2'
    elif skill_class_name == ProtectiveAuraSkill.__name__:
        skill_class = ProtectiveAuraSkill
    elif skill_class_name == HealingRefugeSkill.__name__:
        skill_class = HealingRefugeSkill
    elif skill_class_name == ProtectiveInfusionSkill.__name__:
        skill_class = ProtectiveInfusionSkill
    elif skill_class_name == BeatifyingAegisSkill.__name__:
        skill_class = BeatifyingAegisSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


HEALER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    HealingTouchSkill,
    HealingHerbSkill,
    VitalityAuraSkill,
    ReviveRitualSkill,

    # SKILL2
    ProtectiveAuraSkill,
    HealingRefugeSkill,
    ProtectiveInfusionSkill,
    BeatifyingAegisSkill,
]
HEALER_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

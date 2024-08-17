from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.healer.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    HealingHerbSkill,
    HealingTouchSkill,
    ProtectiveAuraSkill,
    ReviveRitualSkill,
    VitalityAuraSkill,
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
    elif skill_class_name == ProtectiveAuraSkill.__name__:
        skill_class = ProtectiveAuraSkill
    elif skill_class_name == ReviveRitualSkill.__name__:
        skill_class = ReviveRitualSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


HEALER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    HealingTouchSkill,
    HealingHerbSkill,
    VitalityAuraSkill,
    ProtectiveAuraSkill,
    ReviveRitualSkill,
]
HEALER_SKILL_WAYS: List[dict] = [
    skill_way1,
]

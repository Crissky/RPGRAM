from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.cleric.skill1 import (
    AnansisTrickerySkill,
    HecatesFlamesSkill,
    IdunnsAppleSkill,
    IsissVeilSkill,
    KratossWrathSkill,
    OgunsCloakSkill,
    UllrsFocusSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def cleric_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == IdunnsAppleSkill.__name__:
        skill_class = IdunnsAppleSkill
    elif skill_class_name == KratossWrathSkill.__name__:
        skill_class = KratossWrathSkill
    elif skill_class_name == UllrsFocusSkill.__name__:
        skill_class = UllrsFocusSkill
    elif skill_class_name == HecatesFlamesSkill.__name__:
        skill_class = HecatesFlamesSkill
    elif skill_class_name == OgunsCloakSkill.__name__:
        skill_class = OgunsCloakSkill
    elif skill_class_name == IsissVeilSkill.__name__:
        skill_class = IsissVeilSkill
    elif skill_class_name == AnansisTrickerySkill.__name__:
        skill_class = AnansisTrickerySkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


CLERIC_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    IdunnsAppleSkill,
    KratossWrathSkill,
    UllrsFocusSkill,
    HecatesFlamesSkill,
    OgunsCloakSkill,
    IsissVeilSkill,
    AnansisTrickerySkill,
]

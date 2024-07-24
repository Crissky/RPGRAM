from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.cleric.skill1 import (
    AnansisTrickerySkill,
    ArtemissArrowSkill,
    CeridwensMagicPotionSkill,
    GraceOfThePantheonSkill,
    HecatesFlamesSkill,
    IdunnsAppleSkill,
    IsissVeilSkill,
    KratossWrathSkill,
    OgunsCloakSkill,
    UllrsFocusSkill,
    VidarsBraverySkill
)
from rpgram.skills.classes.cleric.skill2 import (
    ConcealmentSkill,
    DhanvantarisAmritaSkill,
    DivinePunishmentSkill,
    HolyFireSkill,
    IxChelsAmphoraSkill
)
from rpgram.skills.classes.cleric.skill3 import (
    GreekFireSkill,
    WillOTheWispSkill
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
    elif skill_class_name == VidarsBraverySkill.__name__:
        skill_class = VidarsBraverySkill
    elif skill_class_name == ArtemissArrowSkill.__name__:
        skill_class = ArtemissArrowSkill
    elif skill_class_name == CeridwensMagicPotionSkill.__name__:
        skill_class = CeridwensMagicPotionSkill
    elif skill_class_name == GraceOfThePantheonSkill.__name__:
        skill_class = GraceOfThePantheonSkill
    # SKILL2
    elif skill_class_name == IxChelsAmphoraSkill.__name__:
        skill_class = IxChelsAmphoraSkill
    elif skill_class_name == DhanvantarisAmritaSkill.__name__:
        skill_class = DhanvantarisAmritaSkill
    elif skill_class_name == ConcealmentSkill.__name__:
        skill_class = ConcealmentSkill
    elif skill_class_name == HolyFireSkill.__name__:
        skill_class = HolyFireSkill
    elif skill_class_name == DivinePunishmentSkill.__name__:
        skill_class = DivinePunishmentSkill
    # SKILL3
    elif skill_class_name == WillOTheWispSkill.__name__:
        skill_class = WillOTheWispSkill
    elif skill_class_name == GreekFireSkill.__name__:
        skill_class = GreekFireSkill
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
    VidarsBraverySkill,
    ArtemissArrowSkill,
    CeridwensMagicPotionSkill,
    GraceOfThePantheonSkill,

    # SKILL2
    IxChelsAmphoraSkill,
    DhanvantarisAmritaSkill,
    ConcealmentSkill,
    HolyFireSkill,
    DivinePunishmentSkill,

    # SKILL3
    WillOTheWispSkill,
    GreekFireSkill,
]

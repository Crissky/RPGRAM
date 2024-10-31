from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.berserkir.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DevastatingRushSkill,
    ImpetuousStrikeSkill,
    IndomitableAttackSkill
)
from rpgram.skills.classes.berserkir.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    FenrirsInstinctSkill,
    FrostBiteSkill,
    HrungnirsSovereigntySkill,
    StoneStrikeSkill,
    YmirsResilienceSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def berserkir_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == IndomitableAttackSkill.__name__:
        skill_class = IndomitableAttackSkill
    elif skill_class_name == ImpetuousStrikeSkill.__name__:
        skill_class = ImpetuousStrikeSkill
    elif skill_class_name == DevastatingRushSkill.__name__:
        skill_class = DevastatingRushSkill
    # SKILL2
    elif skill_class_name == HrungnirsSovereigntySkill.__name__:
        skill_class = HrungnirsSovereigntySkill
    elif skill_class_name == FenrirsInstinctSkill.__name__:
        skill_class = FenrirsInstinctSkill
    elif skill_class_name == YmirsResilienceSkill.__name__:
        skill_class = YmirsResilienceSkill
    elif skill_class_name == StoneStrikeSkill.__name__:
        skill_class = StoneStrikeSkill
    elif skill_class_name == FrostBiteSkill.__name__:
        skill_class = FrostBiteSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BERSERKIR_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    IndomitableAttackSkill,
    ImpetuousStrikeSkill,
    DevastatingRushSkill,

    # SKILL2
    HrungnirsSovereigntySkill,
    FenrirsInstinctSkill,
    YmirsResilienceSkill,
    StoneStrikeSkill,
    FrostBiteSkill,
]
BERSERKIR_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.bounty_hunter.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    ChompTrapSkill,
    HuntingNetSkill,
    InvestigationSkill,
    QuickDrawSkill,
    SharpFaroSkill,
    StabSkill,
    SurpriseAttackSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def bounty_hunter_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == StabSkill.__name__:
        skill_class = StabSkill
    elif skill_class_name == QuickDrawSkill.__name__:
        skill_class = QuickDrawSkill
    elif skill_class_name == SurpriseAttackSkill.__name__:
        skill_class = SurpriseAttackSkill
    elif skill_class_name == HuntingNetSkill.__name__:
        skill_class = HuntingNetSkill
    elif skill_class_name == ChompTrapSkill.__name__:
        skill_class = ChompTrapSkill
    elif skill_class_name == SharpFaroSkill.__name__:
        skill_class = SharpFaroSkill
    elif skill_class_name == InvestigationSkill.__name__:
        skill_class = InvestigationSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BOUNTY_HUNTER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    StabSkill,
    QuickDrawSkill,
    SurpriseAttackSkill,
    HuntingNetSkill,
    ChompTrapSkill,
    SharpFaroSkill,
    InvestigationSkill,
]
BOUNTY_HUNTER_SKILL_WAYS: List[dict] = [
    skill_way1,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.knight.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    ChampionInspirationSkill,
    ChargeSkill,
    HeavyChargeSkill,
    LeadershipSkill,
    SuperChargeSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def knight_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == ChargeSkill.__name__:
        skill_class = ChargeSkill
    elif skill_class_name == HeavyChargeSkill.__name__:
        skill_class = HeavyChargeSkill
    elif skill_class_name == SuperChargeSkill.__name__:
        skill_class = SuperChargeSkill
    elif skill_class_name == ChampionInspirationSkill.__name__:
        skill_class = ChampionInspirationSkill
    elif skill_class_name == LeadershipSkill.__name__:
        skill_class = LeadershipSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


KNIGHT_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    ChargeSkill,
    HeavyChargeSkill,
    SuperChargeSkill,
    ChampionInspirationSkill,
    LeadershipSkill,
]
KNIGHT_SKILL_WAYS: List[dict] = [
    skill_way1,
]

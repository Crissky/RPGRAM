from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.multiclasse.precision_attack import (
    QuickAttackSkill
)
from rpgram.skills.classes.weapon_master.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    BruisingAttackSkill,
    SlashingAttackSkill,
    TerrebrantAttackSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def weapon_master_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == SlashingAttackSkill.__name__:
        skill_class = SlashingAttackSkill
    elif skill_class_name == BruisingAttackSkill.__name__:
        skill_class = BruisingAttackSkill
    elif skill_class_name == TerrebrantAttackSkill.__name__:
        skill_class = TerrebrantAttackSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


WEAPON_MASTER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    SlashingAttackSkill,
    BruisingAttackSkill,
    TerrebrantAttackSkill,
]
WEAPON_MASTER_SKILL_WAYS: List[dict] = [
    skill_way1,
]

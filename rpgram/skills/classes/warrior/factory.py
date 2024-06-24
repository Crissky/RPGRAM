from typing import TYPE_CHECKING
from rpgram.skills.classes.warrior.skill1 import (
    PowerfulAttackSkill
)
from rpgram.skills.classes.warrior.skill2 import (
    LethalAttackSkill,
    QuickAttackSkill
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
    # SKILL2
    elif skill_class_name == QuickAttackSkill.__name__:
        skill_class = QuickAttackSkill
    elif skill_class_name == LethalAttackSkill.__name__:
        skill_class = LethalAttackSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


WARRIOR_SKILL_LIST = [
    # SKILL1
    PowerfulAttackSkill,

    # SKILL2
    QuickAttackSkill,
    LethalAttackSkill,
]

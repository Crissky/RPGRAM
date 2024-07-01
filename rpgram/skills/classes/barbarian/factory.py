from typing import TYPE_CHECKING
from rpgram.skills.classes.barbarian.skill1 import (
    FuriousAttackSkill,
    WildStrikeSkill
)
from rpgram.skills.classes.barbarian.skill2 import (
    FuriousFurySkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def barbarian_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == FuriousAttackSkill.__name__:
        skill_class = FuriousAttackSkill
    elif skill_class_name == WildStrikeSkill.__name__:
        skill_class = WildStrikeSkill
    # SKILL2
    elif skill_class_name == FuriousFurySkill.__name__:
        skill_class = FuriousFurySkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BARBARIAN_SKILL_LIST = [
    # SKILL1
    FuriousAttackSkill,
    WildStrikeSkill,

    # SKILL2
    FuriousFurySkill,
]

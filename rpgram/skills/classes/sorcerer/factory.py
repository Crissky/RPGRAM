from typing import TYPE_CHECKING
from rpgram.skills.classes.sorcerer.skill1 import (
    MysticalConfluenceSkill,
    MysticalProtectionSkill,
    MysticalVigorSkill
)
from rpgram.skills.classes.sorcerer.skill2 import (
    PrismaticScintillationSkill,
    PrismaticShotSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def sorcerer_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == MysticalProtectionSkill.__name__:
        skill_class = MysticalProtectionSkill
    elif skill_class_name == MysticalConfluenceSkill.__name__:
        skill_class = MysticalConfluenceSkill
    elif skill_class_name == MysticalVigorSkill.__name__:
        skill_class = MysticalVigorSkill
    # SKILL2
    elif skill_class_name == PrismaticShotSkill.__name__:
        skill_class = PrismaticShotSkill
    elif skill_class_name == PrismaticScintillationSkill.__name__:
        skill_class = PrismaticScintillationSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SORCERER_SKILL_LIST = [
    # SKILL1
    MysticalProtectionSkill,
    MysticalConfluenceSkill,
    MysticalVigorSkill,

    # SKILL2
    PrismaticShotSkill,
    PrismaticScintillationSkill,
]

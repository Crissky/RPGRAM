from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.sorcerer.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    MysticalConfluenceSkill,
    MysticalProtectionSkill,
    MysticalVigorSkill
)
from rpgram.skills.classes.sorcerer.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    PrismaticScintillationSkill,
    PrismaticShieldSkill,
    PrismaticShotSkill
)
from rpgram.skills.classes.sorcerer.skill3 import (
    SKILL_WAY_DESCRIPTION as skill_way3,
    ChaosOrbSkill,
    ChaosVampirismSkill,
    ChaosWeaverSkill
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
    elif skill_class_name == PrismaticShieldSkill.__name__:
        skill_class = PrismaticShieldSkill
    # SKILL3
    elif skill_class_name == ChaosOrbSkill.__name__:
        skill_class = ChaosOrbSkill
    elif skill_class_name == ChaosVampirismSkill.__name__:
        skill_class = ChaosVampirismSkill
    elif skill_class_name == ChaosWeaverSkill.__name__:
        skill_class = ChaosWeaverSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SORCERER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    MysticalProtectionSkill,
    MysticalConfluenceSkill,
    MysticalVigorSkill,

    # SKILL2
    PrismaticShotSkill,
    PrismaticScintillationSkill,
    PrismaticShieldSkill,

    # SKILL3
    ChaosOrbSkill,
    ChaosVampirismSkill,
    ChaosWeaverSkill,
]
SORCERER_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
    skill_way3,
]

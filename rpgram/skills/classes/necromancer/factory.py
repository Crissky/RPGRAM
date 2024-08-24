from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.necromancer.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    AbyssalCreatureSkill,
    BannedSoulSkill,
    TheHordeSkill,
    UndeadEmbraceSkill,
    VengefulSpiritSkill
)
from rpgram.skills.classes.necromancer.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    BoneArmorSkill,
    BoneBucklerSkill,
    BoneSpaulderSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def necromancer_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == BannedSoulSkill.__name__:
        skill_class = BannedSoulSkill
    elif skill_class_name == VengefulSpiritSkill.__name__:
        skill_class = VengefulSpiritSkill
    elif skill_class_name == UndeadEmbraceSkill.__name__:
        skill_class = UndeadEmbraceSkill
    elif skill_class_name == AbyssalCreatureSkill.__name__:
        skill_class = AbyssalCreatureSkill
    elif skill_class_name == TheHordeSkill.__name__:
        skill_class = TheHordeSkill
    # SKILL2
    elif skill_class_name == BoneBucklerSkill.__name__:
        skill_class = BoneBucklerSkill
    elif skill_class_name == BoneSpaulderSkill.__name__:
        skill_class = BoneSpaulderSkill
    elif skill_class_name == BoneArmorSkill.__name__:
        skill_class = BoneArmorSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


NECROMANCER_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    BannedSoulSkill,
    VengefulSpiritSkill,
    UndeadEmbraceSkill,
    AbyssalCreatureSkill,
    TheHordeSkill,
    # SKILL2
    BoneBucklerSkill,
    BoneSpaulderSkill,
    BoneArmorSkill,
]
NECROMANCER_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

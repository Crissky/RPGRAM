from typing import TYPE_CHECKING, List, Type

from rpgram.skills.classes.paladin.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    BlueDjinnBalmSkill,
    CourtesanAnointingSkill,
    GreenDragonBalmSkill,
    KnightAnointingSkill,
    LordAnointingSkill,
    MaidenAnointingSkill,
    RedPhoenixBalmSkill,
    SquireAnointingSkill,
    SacredBalmSkill,
    WarriorAnointingSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def paladin_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == SacredBalmSkill.__name__:
        skill_class = SacredBalmSkill
    elif skill_class_name == GreenDragonBalmSkill.__name__:
        skill_class = GreenDragonBalmSkill
    elif skill_class_name == RedPhoenixBalmSkill.__name__:
        skill_class = RedPhoenixBalmSkill
    elif skill_class_name == BlueDjinnBalmSkill.__name__:
        skill_class = BlueDjinnBalmSkill
    elif skill_class_name == SquireAnointingSkill.__name__:
        skill_class = SquireAnointingSkill
    elif skill_class_name == WarriorAnointingSkill.__name__:
        skill_class = WarriorAnointingSkill
    elif skill_class_name == MaidenAnointingSkill.__name__:
        skill_class = MaidenAnointingSkill
    elif skill_class_name == KnightAnointingSkill.__name__:
        skill_class = KnightAnointingSkill
    elif skill_class_name == CourtesanAnointingSkill.__name__:
        skill_class = CourtesanAnointingSkill
    elif skill_class_name == LordAnointingSkill.__name__:
        skill_class = LordAnointingSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


PALADIN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    SacredBalmSkill,
    GreenDragonBalmSkill,
    RedPhoenixBalmSkill,
    BlueDjinnBalmSkill,
    SquireAnointingSkill,
    WarriorAnointingSkill,
    MaidenAnointingSkill,
    KnightAnointingSkill,
    CourtesanAnointingSkill,
    LordAnointingSkill,
]
PALADIN_SKILL_WAYS: List[dict] = [
    skill_way1,
]

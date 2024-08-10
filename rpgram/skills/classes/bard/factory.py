from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.bard.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    DissonanceSkill,
    FatalChordSkill,
    ResonanceSkill,
    SupersonicSkill
)
from rpgram.skills.classes.bard.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    CrescentMoonBalladSkill,
    InvigoratingSongSkill,
    TricksterTrovaSkill,
    WarSongSkill,
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def bard_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == DissonanceSkill.__name__:
        skill_class = DissonanceSkill
    elif skill_class_name == ResonanceSkill.__name__:
        skill_class = ResonanceSkill
    elif skill_class_name == FatalChordSkill.__name__:
        skill_class = FatalChordSkill
    elif skill_class_name == SupersonicSkill.__name__:
        skill_class = SupersonicSkill
    # SKILL2
    elif skill_class_name == WarSongSkill.__name__:
        skill_class = WarSongSkill
    elif skill_class_name == CrescentMoonBalladSkill.__name__:
        skill_class = CrescentMoonBalladSkill
    elif skill_class_name == TricksterTrovaSkill.__name__:
        skill_class = TricksterTrovaSkill
    elif skill_class_name == InvigoratingSongSkill.__name__:
        skill_class = InvigoratingSongSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BARD_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    DissonanceSkill,
    ResonanceSkill,
    FatalChordSkill,
    SupersonicSkill,
    WarSongSkill,
    CrescentMoonBalladSkill,
    TricksterTrovaSkill,
    InvigoratingSongSkill,
]
BARD_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.shaman.skill1 import (
    SKILL_WAY_DESCRIPTION as skill_way1,
    CrystalSapRingSkill,
    VineCrosierSkill,
    WildCarnationCloakSkill,
)
from rpgram.skills.classes.shaman.skill2 import (
    SKILL_WAY_DESCRIPTION as skill_way2,
    ClairvoyantWolfSkill,
    FighterPandinusSkill,
    LookouterYetiSkill,
    ProtectorTurtleSkill
)
from rpgram.skills.skill_base import BaseSkill


if TYPE_CHECKING:
    from rpgram.characters.char_base import BaseCharacter


def shaman_skill_factory(
    skill_class_name: str,
    char: 'BaseCharacter',
    level: int = 1
) -> BaseSkill:
    # SKILL1
    if skill_class_name == VineCrosierSkill.__name__:
        skill_class = VineCrosierSkill
    elif skill_class_name == WildCarnationCloakSkill.__name__:
        skill_class = WildCarnationCloakSkill
    elif skill_class_name == CrystalSapRingSkill.__name__:
        skill_class = CrystalSapRingSkill
    elif skill_class_name == FighterPandinusSkill.__name__:
        skill_class = FighterPandinusSkill
    elif skill_class_name == ProtectorTurtleSkill.__name__:
        skill_class = ProtectorTurtleSkill
    elif skill_class_name == ClairvoyantWolfSkill.__name__:
        skill_class = ClairvoyantWolfSkill
    elif skill_class_name == LookouterYetiSkill.__name__:
        skill_class = LookouterYetiSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


SHAMAN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    VineCrosierSkill,
    WildCarnationCloakSkill,
    CrystalSapRingSkill,
    FighterPandinusSkill,
    ProtectorTurtleSkill,
    ClairvoyantWolfSkill,
    LookouterYetiSkill,
]
SHAMAN_SKILL_WAYS: List[dict] = [
    skill_way1,
    skill_way2,
]

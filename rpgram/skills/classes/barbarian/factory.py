from typing import TYPE_CHECKING, List, Type
from rpgram.skills.classes.barbarian.skill1 import (
    PrimalAttackSkill,
    SeismicImpactSkill,
    PrimalRamSkill,
    PrimalStrikeSkill
)
from rpgram.skills.classes.barbarian.skill2 import (
    FrenzySkill,
    FuriousFurySkill,
    FuriousInstinctSkill,
    FuriousRoarSkill
)
from rpgram.skills.classes.barbarian.skill3 import (
    FafnirsScalesSkill,
    HydraFangsSkill,
    RaijusFootstepsSkill,
    SalamandersBreathSkill,
    SweepingRocSkill,
    WildForgeSkill
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
    if skill_class_name == PrimalAttackSkill.__name__:
        skill_class = PrimalAttackSkill
    elif skill_class_name == PrimalStrikeSkill.__name__:
        skill_class = PrimalStrikeSkill
    elif skill_class_name == PrimalRamSkill.__name__:
        skill_class = PrimalRamSkill
    elif skill_class_name == SeismicImpactSkill.__name__:
        skill_class = SeismicImpactSkill
    # SKILL2
    elif skill_class_name == FuriousFurySkill.__name__:
        skill_class = FuriousFurySkill
    elif skill_class_name == FuriousInstinctSkill.__name__:
        skill_class = FuriousInstinctSkill
    elif skill_class_name == FrenzySkill.__name__:
        skill_class = FrenzySkill
    elif skill_class_name == FuriousRoarSkill.__name__:
        skill_class = FuriousRoarSkill
    # SKILL3
    elif skill_class_name == WildForgeSkill.__name__:
        skill_class = WildForgeSkill
    elif skill_class_name == SalamandersBreathSkill.__name__:
        skill_class = SalamandersBreathSkill
    elif skill_class_name == SweepingRocSkill.__name__:
        skill_class = SweepingRocSkill
    elif skill_class_name == HydraFangsSkill.__name__:
        skill_class = HydraFangsSkill
    elif skill_class_name == RaijusFootstepsSkill.__name__:
        skill_class = RaijusFootstepsSkill
    elif skill_class_name == FafnirsScalesSkill.__name__:
        skill_class = FafnirsScalesSkill
    else:
        raise ValueError(f'Skill {skill_class_name} não encontrada!')

    return skill_class(char, level)


BARBARIAN_SKILL_LIST: List[Type[BaseSkill]] = [
    # SKILL1
    PrimalAttackSkill,
    PrimalStrikeSkill,
    PrimalRamSkill,
    SeismicImpactSkill,

    # SKILL2
    FuriousFurySkill,
    FuriousInstinctSkill,
    FrenzySkill,
    FuriousRoarSkill,
    
    # SKILL3
    WildForgeSkill,
    SalamandersBreathSkill,
    SweepingRocSkill,
    HydraFangsSkill,
    RaijusFootstepsSkill,
    FafnirsScalesSkill,
]
